import sys
import unittest

import cardtest
import gametest
import playertest
import shuffletest

loader = unittest.TestLoader()
suite  = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(cardtest))
suite.addTests(loader.loadTestsFromModule(gametest))
suite.addTests(loader.loadTestsFromModule(playertest))
suite.addTests(loader.loadTestsFromModule(shuffletest))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)

#return 1 if there all test are successful otherwise 0
sys.exit(len(result.errors) == 0)