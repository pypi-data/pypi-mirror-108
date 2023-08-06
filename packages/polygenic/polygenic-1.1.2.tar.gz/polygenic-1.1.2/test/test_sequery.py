from unittest import TestCase
from polygenic import polygenic

class TestSequery(TestCase):
    def testCommandLine(self):
        polygenic.main(["--vcf", "/home/marpiech/data/clustered_204800980122_R01C02.vcf.gz", "--af", "/home/marpiech/data/af.vcf.gz", "--log_file", "/dev/null", "--models_and_descriptions_path", "polygenic/resources/models", "--population", "eas", "--out_dir", "/tmp/polygenic"])
        self.assertEqual('1', '1')

if __name__ == "__main__":
    unittest.main()
