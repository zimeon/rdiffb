"""Shell calls to test command line client rdiffb.py."""
import unittest
import subprocess


def run(args_str):
    """Call code and return exit value."""
    return(subprocess.call("python rdfdiffb.py " + args_str, shell=True))


class TestCommandLineClient(unittest.TestCase):
    """Command line client tests."""

    def test01_simple_matches(self):
        """Test graphs that should match, exit code 0."""
        self.assertEqual(run("testdata/graph2_a.n3 testdata/graph2_b.n3"), 0)

    def test02_simple_mismatches(self):
        """Test graphs that should not match, exit code 1."""
        self.assertEqual(run("testdata/graph1_a.ttl testdata/graph2_b.n3"), 1)

    def test03_match_after_bnode_sub(self):
        """Test graphs that should match only with some nodes mapped to bnodes."""
        # Mismatch because subjects are /gen1 and /gen2
        self.assertEqual(run("testdata/graph3_a.ttl testdata/graph3_b.ttl"), 1)
        # Match if we make /gen1 and /gen2 into bnodes
        self.assertEqual(run("testdata/graph3_a.ttl testdata/graph3_b.ttl " +
                             "--bnode '/gen1' --bnode='/gen2'"), 0)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCommandLineClient)
    unittest.TextTestRunner(verbosity=2).run(suite)
