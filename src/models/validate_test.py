def print_rule (rule): 

    print (f"\n\nRule ID: {rule['rule_id']}")
    print (f"Titulo: {rule['title']}")
    test_number =1
    for test in rule["tests"]: #Tests
      print (f"\n\tTest {test_number}")
      print(f"\tTest type: {test['test_type']}")
      print(f"\tTest comment: {test['test_comment']}")
      print(f"\tTest state: {test['state']}")
      print(f"\tTest comment: {test['state_comment']}")
      print ("\tCOMMANDS: ")
      com_number = 1
      for proof in test['tests_dictionary']: #commands
        print (f"\tFrom test {test_number} Command number: {com_number}")
        print(f"\tcommand: {proof['test']}")
        print(f"\tcomment: {proof['comment']}")
        com_number = com_number+1
      test_number = test_number+1


def dpkginfo_test(result, rule_test_comment):
    #print (f'Resultado: {result}')
    #print (f'Prueba: {rule_test_comment}')
    is_in_result = False
    is_expected = True
    if result == '': 
        is_in_result = True
    if 'is not installed' in rule_test_comment :
        is_expected = False
    return is_expected == is_in_result


def textfilecontent54_test(result, test, proof):

    state = test['state']
    comment = test['state_comment']

    if  "No such file or directory" in result: 
        return False
    
    elif "Permission denied" in result: 
        return False
    
    elif state in result:
        return True
    
    else: 
        print (f"\n\nResult {result}")
        print (f"test {test}")
        print (f"Proof {proof}") 

    return False
