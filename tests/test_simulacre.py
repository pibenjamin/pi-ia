"""Tests des scripts par règles. Ils fixent le comportement attendu sur les données fictives,
ce qui rend la démonstration reproductible (même sans IA)."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "scripts"))

import backlog  # noqa: E402
import capacite  # noqa: E402
import commun as c  # noqa: E402
import dependances  # noqa: E402
import evaluer  # noqa: E402
import release  # noqa: E402
import signaux  # noqa: E402
import flux  # noqa: E402


class Donnees(unittest.TestCase):
    def test_douze_domaines_avec_equipe_referente_connue(self):
        doms = c.domaines()
        self.assertEqual(len(doms), 12)
        self.assertTrue(all(d["equipe_referente"] in c.equipes() for d in doms.values()))

    def test_epiques_bien_formees(self):
        eps = c.epiques()
        self.assertTrue(15 <= len(eps) <= 20)
        doms = c.domaines()
        for e in eps:
            self.assertTrue(set(e["domaines"]) <= set(doms), e["id"])
            self.assertTrue(all(0 <= v <= 100 for v in e["domaines"].values()), e["id"])
            self.assertEqual(Path(e["fichier"]).stem, e["id"])

    def test_anonymisation(self):
        r = subprocess.run([sys.executable, str(RACINE / "scripts/anonymiser.py"), "verifier"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)


class Capacite(unittest.TestCase):
    def test_etats(self):
        r = capacite.calculer("2027-T1")["equipes"]
        self.assertEqual(r["EQ-C"]["etat"], "surcharge")
        self.assertEqual(r["EQ-E"]["etat"], "surcharge")
        self.assertTrue(r["EQ-D"]["alerte_non_disponible"])
        self.assertEqual(r["EQ-B"]["etat"], "ok")

    def test_epique_sans_equipe_hors_charge(self):
        r = capacite.calculer("2027-T1")
        self.assertEqual([x["epique"] for x in r["epiques_sans_equipe"]], ["EP-603"])


class Dependances(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = dependances.analyser("2027-T1", "2026-S48")
        cls.ids = {s["id"] for s in cls.r["signaux"]}

    def test_feature_deja_livree_ecartee(self):
        self.assertNotIn("DEP-EP-502-EQ-A", self.ids)
        self.assertIn("EP-502", [x["epique"] for x in self.r["ecartes"]])

    def test_certitude_faible_ignoree(self):
        self.assertNotIn("DEP-EP-101-EQ-E", self.ids)
        self.assertNotIn("DEP-EP-202-EQ-F", self.ids)

    def test_epique_hors_trimestre_ignoree(self):
        self.assertFalse(any(s["epique"] == "EP-403" for s in self.r["signaux"]))

    def test_types(self):
        s = {x["id"]: x for x in self.r["signaux"]}
        self.assertIn("capacite-charge", s["DEP-EP-201-EQ-C"]["types"])
        self.assertIn("connaissance", s["DEP-EP-401-EQ-F"]["types"])
        self.assertIn("sequence-coordination", s["DEP-EP-303-EQ-D"]["types"])

    def test_format_valide(self):
        self.assertEqual(signaux.erreurs_format(self.r), [])

    def test_evaluation_tracable(self):
        e = evaluer.evaluer(self.r)
        self.assertEqual(e["nb_trouvees"], 8)
        self.assertEqual(e["manquees"], ["GT-08"])  # domaine non coché : manqué par les règles
        self.assertEqual(e["nb_faux_positifs"], 3)
        self.assertEqual(e["calibration"]["haute"]["faux_positifs"], 0)

    def test_bonne_equipe_mauvaise_raison_ne_compte_pas(self):
        e = evaluer.evaluer(self.r)
        v = {x["id"]: x for x in e["signaux"]}
        self.assertEqual(v["DEP-EP-302-EQ-F"]["verdict"], "faux positif")


class Format(unittest.TestCase):
    def test_signal_invalide_detecte(self):
        d = {"semaine": "x", "trimestre": "2027-T1", "source": "ia",
             "signaux": [{"id": "x", "epique": "EP-999", "equipe_cible": "EQ-Z", "domaines": ["DOM-99"],
                          "types": ["autre"], "confiance": "certaine", "criteres": []}]}
        self.assertGreaterEqual(len(signaux.erreurs_format(d)), 5)


class Backlog(unittest.TestCase):
    def test_faiblesses_injectees(self):
        f = backlog.analyser("2027-T1", "2026-S48")["faiblesses"]
        motifs = {(tuple(x["epiques"]), x["motif"]) for x in f}
        self.assertIn((("EP-503",), "trop-grosse"), motifs)
        self.assertIn((("EP-503",), "manque-informations"), motifs)
        self.assertIn((("EP-603",), "ownership-flou"), motifs)
        self.assertIn((("EP-104", "EP-501"), "doublon-potentiel"), motifs)


class FluxEtRelease(unittest.TestCase):
    def test_flux(self):
        r = flux.calculer("2026-S48")
        self.assertGreater(r["equipes"]["EQ-C"]["wip"], r["equipes"]["EQ-C"]["limite_wip"])
        self.assertTrue(any("EQ-E" in a for a in r["alertes"]))

    def test_release_sous_conditions(self):
        e = release.evaluer("R-2027.1")
        self.assertEqual(e["proposition_regles"], "go sous conditions")


class Journal(unittest.TestCase):
    def test_role_exige(self):
        import journal
        with tempfile.TemporaryDirectory() as tmp:
            ancien = c.RACINE
            try:
                # journal écrit relativement à c.RACINE : on le redirige le temps du test
                for d in ("config", "gouvernance"):
                    os.symlink(ancien / d, Path(tmp) / d)
                c.RACINE = Path(tmp)
                code = journal.main(["validation", "--signal", "DEP-EP-102-EQ-F", "--decision", "ecartee",
                                     "--par", "inconnu", "--exiger-role", "TL-"])
                self.assertEqual(code, 2)
                code = journal.main(["validation", "--signal", "DEP-EP-102-EQ-F", "--decision", "ecartee",
                                     "--par", "inconnu"])
                self.assertEqual(code, 0)
                lignes = (Path(tmp) / "validation/journal.csv").read_text().splitlines()
                self.assertEqual(len(lignes), 2)
                self.assertIn("hors-roles", lignes[1])
            finally:
                c.RACINE = ancien


if __name__ == "__main__":
    unittest.main()
