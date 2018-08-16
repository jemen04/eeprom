#! /usr/bin/env python3

import setuppath
import mfgtestfram2 as mfgtestfram


class SampleTest(mfgtestfram.IndividualTest):
    name = "Test Name here"
    # schema no longer used
    schema = { # or could use OrderedDict
        }

    def run_test(self):
        # override run_test() for actual operations
        import pdb;pdb.set_trace()
        # command to equipment manager is accessible using self.em_cmd()
        #self.em_cmd('equipment_name', 'method_name')
        # could take additional args if needed
        #self.em_cmd('equipment_name2', 'method_name2', 1, 2)

        # test limits are available through self.limits
        # with limit names defined at top of class definition
        limit1 = self.limits['limit_name_1']
        limit2 = self.limits['limit_name_2']

        # save test data
        self.result.test_data['data_name'] = 1234

        # error code
        self.result.add_error_code['error_code_name']

        # send console message to user on Semap app
        self.send_msg('message string here')
        
        import pdb;pdb.set_trace()

        # test result are stored in self.results
        if True:
            self.result.passed = True


class Setup(mfgtestfram.IndividualTest):
    name = "Setup"
    def run(self):
        #val = self.em_cmd('equipment_name', 'method_name')
        self.result.test_data['data_name'] = 1234

        self.result.passed = True


class Teardown(mfgtestfram.IndividualTest):
    name = "Teardown"
    def run(self):
        #val = self.em_cmd('equipment_name', 'method_name')
        self.result.test_data['data_name'] = 1234

        self.result.passed = True

# for old mfgtestframe
'''
# make a sequence of tests
class SampleTestSequence:
    known_tests = [SampleTest]
    # or if many tests
    # known_tests = [SampleTest, SampleTest2, SampleTest3]


# to make it a standalone test:
if __name__ == '__main__':
    """
    test = mfgtestfram.Runnable(SampleTest)
    # or to make a standalone test sequence
    # test = mfgtestfram.Runnable(SampleTestSequence)
    test.get_options_cli()
    test.start_equip_client()
    test.run()
    test_result_json = test.get_result_json(indent=3)
   """
'''

# to make it a standalone test:
if __name__ == '__main__':
    runnable = mfgtestfram.Runnable()
    runnable.load_available_tests([
        SampleTest
    ], Setup, Teardown)
    runnable.get_options_cli()
    #runnable.start_equip_client()
    runnable.initialize()
    runnable.run(exit_if_unknown_test=False)
    runnable.finalize()
