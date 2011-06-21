#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import Entity, Status, StatusList, Project
from stalker.ext.validatedList import ValidatedList



########################################################################
class StatusTest(mocker.MockerTestCase):
    """tests the status class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.kwargs = {
            "name": "Complete",
            "description": "use this when the object is complete",
            "code": "CMPLT",
        }
        
        # create an entity object with same kwargs for __eq__ and __ne__ tests
        # (it should return False for __eq__ and True for __ne__ for same
        # kwargs)
        self.entity1 = Entity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality of two statuses
        """
        
        status1 = Status(**self.kwargs)
        status2 = Status(**self.kwargs)
        
        self.kwargs["name"] = "Work In Progress"
        self.kwargs["description"] = "use this when the object is still in \
        progress"
        self.kwargs["code"] = "WIP"
        
        status3 = Status(**self.kwargs)
        
        self.assertTrue(status1==status2)
        self.assertFalse(status1==status3)
        self.assertFalse(status1==self.entity1)
    
    
    
    #----------------------------------------------------------------------
    def test_status_and_string_equality_in_status_name(self):
        """testing a status can be compared with a string and returns True if
        the string matches the name and vice versa
        """
        
        a_status = Status(**self.kwargs)
        self.assertTrue(a_status==self.kwargs["name"])
        self.assertTrue(a_status==self.kwargs["name"].lower())
        self.assertTrue(a_status==self.kwargs["name"].upper())
        self.assertTrue(a_status==unicode(self.kwargs["name"]))
        self.assertTrue(a_status==unicode(self.kwargs["name"].lower()))
        self.assertTrue(a_status==unicode(self.kwargs["name"].upper()))
        self.assertFalse(a_status=="another name")
        self.assertFalse(a_status==u"another name")
    
    
    
    #----------------------------------------------------------------------
    def test_status_and_string_equality_in_status_code(self):
        """testing a status can be compared with a string and returns True if
        the string matches the code and vice versa
        """
        
        a_status = Status(**self.kwargs)
        self.assertTrue(a_status==self.kwargs["code"])
        self.assertTrue(a_status==self.kwargs["code"].lower())
        self.assertTrue(a_status==self.kwargs["code"].upper())
        self.assertTrue(a_status==unicode(self.kwargs["code"]))
        self.assertTrue(a_status==unicode(self.kwargs["code"].lower()))
        self.assertTrue(a_status==unicode(self.kwargs["code"].upper()))
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing inequality of two statuses
        """
        
        status1 = Status(**self.kwargs)
        status2 = Status(**self.kwargs)
        
        self.kwargs["name"] = "Work In Progress"
        self.kwargs["description"] = "use this when the object is still in \
        progress"
        self.kwargs["code"] = "WIP"
        
        status3 = Status(**self.kwargs)
        
        self.assertFalse(status1!=status2)
        self.assertTrue(status1!=status3)
        self.assertTrue(status1!=self.entity1)
    
    
    #----------------------------------------------------------------------
    def test_status_and_string_inequality_in_status_name(self):
        """testing a status can be compared with a string and returns False if
        the string matches the name and vice versa
        """
        
        a_status = Status(**self.kwargs)
        self.assertFalse(a_status!=self.kwargs["name"])
        self.assertFalse(a_status!=self.kwargs["name"].lower())
        self.assertFalse(a_status!=self.kwargs["name"].upper())
        self.assertFalse(a_status!=unicode(self.kwargs["name"]))
        self.assertFalse(a_status!=unicode(self.kwargs["name"].lower()))
        self.assertFalse(a_status!=unicode(self.kwargs["name"].upper()))
        self.assertTrue(a_status!="another name")
        self.assertTrue(a_status!=u"another name")
    
    
    
    #----------------------------------------------------------------------
    def test_status_and_string_inequality_in_status_code(self):
        """testing a status can be compared with a string and returns False if
        the string matches the code and vice versa
        """
        
        a_status = Status(**self.kwargs)
        self.assertFalse(a_status!=self.kwargs["code"])
        self.assertFalse(a_status!=self.kwargs["code"].lower())
        self.assertFalse(a_status!=self.kwargs["code"].upper())
        self.assertFalse(a_status!=unicode(self.kwargs["code"]))
        self.assertFalse(a_status!=unicode(self.kwargs["code"].lower()))
        self.assertFalse(a_status!=unicode(self.kwargs["code"].upper()))








########################################################################
class StatusListTest(mocker.MockerTestCase):
    """testing the StatusList class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """let's create proper values for the tests
        """
        
        self.kwargs = {
            "name": "a status list",
            "description": "this is a status list for testing purposes",
            "statuses": [
                Status(name="Not Available", code="N/A"),
                Status(name="Waiting To Start", code="WSTRT"),
                Status(name="Started", code="STRT"),
                Status(name="Waiting For Approve", code="WAPPR"),
                Status(name="Approved", code="APPR"),
                Status(name="Finished", code="FNSH"),
                Status(name="On Hold", code="OH"),
                ],
            "target_entity_type": Project.entity_type,
        }
        
        self.mock_status_list = StatusList(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_statuses_argument_accepts_statuses_only(self):
        """testing if statuses list argument accepts list of statuses only
        """
        
        # the statuses argument should be a list of statuses
        # can be empty?
        #
        
        test_values = ["a str", {}, 1, 1.0]
        
        for test_value in test_values:
            #----------------------------------------
            # it should only accept lists of statuses
            
            self.kwargs["statuses"] = test_value
            
            self.assertRaises(TypeError, StatusList, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_statuses_attribute_accepting_only_statuses(self):
        """testing the status_list attribute accepting Status objects only
        """
        
        test_values = ["1", ["1"], 1, [1, "w"]]
        
        # check the attribute
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_status_list,
                "statuses",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_statuses_being_empty(self):
        """testing status_list against being empty
        """
        
        #----------------------------------------------------------------------
        # the list couldn't be empty
        self.kwargs["statuses"] = []
        
        self.assertRaises(ValueError, StatusList, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_statuses_elements_being_status_objects(self):
        """testing status_list elements against not being derived from Status
        class
        """
        
        #------------------------------------------------------
        # every element should be an object derived from Status
        a_fake_status_list = [1, 2, "a string", u"a unicode", 4.5]
        
        self.kwargs["statuses"] = a_fake_status_list
        
        self.assertRaises(TypeError, StatusList, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_statuses_attribute_works_properly(self):
        """testing if status_list attribute is working properly
        """
        
        new_list_of_statutes = [
            Status(name="New Status", code="NSTS")
        ]
        
        self.mock_status_list.statuses = new_list_of_statutes
        self.assertEqual( self.mock_status_list.statuses,
                           new_list_of_statutes)
    
    
    
    #----------------------------------------------------------------------
    def test_statuses_attributes_elements_changed_to_none_status_objects(self):
        """testing if a TypeError will be raised when trying to set an
        individual element in the statuses list to an object which is not a
        Status instance
        """
        
        self.assertRaises(
            TypeError,
            self.mock_status_list.statuses.__setitem__,
            0,
            0
        )
    
    
    
    #----------------------------------------------------------------------
    def test_statuses_attribute_is_converted_to_ValidatedList(self):
        """testing if the statuses attribute is converted to a ValidetedList
        instance
        """
        
        self.assertIsInstance(self.mock_status_list.statuses,
                                   ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_equality_operator(self):
        """testing equality of two status list object
        """
        
        status_list1 = StatusList(**self.kwargs)
        status_list2 = StatusList(**self.kwargs)
        
        
        self.kwargs["target_entity_type"] = "SomeOtherClass"
        
        status_list3 = StatusList(**self.kwargs)
        
        self.kwargs["statuses"] = [
            Status(name="Started", code="STRT"),
            Status(name="Waiting For Approve", code="WAPPR"),
            Status(name="Approved", code="APPR"),
            Status(name="Finished", code="FNSH"),
        ]
        
        status_list4 = StatusList(**self.kwargs)
        
        
        
        self.assertTrue(status_list1==status_list2)
        self.assertFalse(status_list1==status_list3)
        self.assertFalse(status_list1==status_list4)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality_operator(self):
        """testing equality of two status list object
        """
        
        status_list1 = StatusList(**self.kwargs)
        status_list2 = StatusList(**self.kwargs)
        
        self.kwargs["target_entity_type"] = "SomeOtherClass"
        
        status_list3 = StatusList(**self.kwargs)
        
        self.kwargs["statuses"] = [
            Status(name="Started", code="STRT"),
            Status(name="Waiting For Approve", code="WAPPR"),
            Status(name="Approved", code="APPR"),
            Status(name="Finished", code="FNSH"),
        ]
        
        status_list4 = StatusList(**self.kwargs)
        
        self.assertFalse(status_list1!=status_list2)
        self.assertTrue(status_list1!=status_list3)
        self.assertTrue(status_list1!=status_list4)
    
    
    
    #----------------------------------------------------------------------
    def test_indexing_get(self):
        """testing indexing of statuses in the statusList, get
        """
        # first try indexing
        
        # this shouldn't raise a TypeError
        status1 = self.mock_status_list[0]
        
        # check the equality
        self.assertEqual(self.mock_status_list.statuses[0], status1)
    
    
    
    #----------------------------------------------------------------------
    def test_indexing_get_string_indexes(self):
        """testing indexing of statuses in the statusList, get with string
        """
        
        status1 = Status(name="Complete", code="CMPLT")
        status2 = Status(name="Work in Progress", code="WIP")
        status3 = Status(name="Pending Review", code="PRev")
        
        a_status_list = StatusList(name="Asset Status List",
                                          statuses=[status1, status2, status3],
                                          target_entity_type="Asset")
        
        self.assertEqual(a_status_list[0], a_status_list["complete"])
        self.assertEqual(a_status_list[1], a_status_list["wip"])
    
    
    
    #----------------------------------------------------------------------
    def test_indexing_set(self):
        """testing indexing of statuses in the statusList, set
        """
        # first try indexing
        
        # this shouldn't raise a TypeError
        status1 = self.mock_status_list[0]
        
        self.mock_status_list[-1] = status1
        
        # check the equality
        self.assertEqual(self.mock_status_list.statuses[-1], status1)
    
    
    
    #----------------------------------------------------------------------
    def test_indexing_del(self):
        """testing indexing of statuses in the statusList, del
        """
        
        # first get the lenght
        len_statuses = len(self.mock_status_list.statuses)
        
        del self.mock_status_list[-1]
        
        self.assertEqual(len(self.mock_status_list.statuses),
                          len_statuses-1)
    
    
    
    #----------------------------------------------------------------------
    def test_indexing_len(self):
        """testing indexing of statuses in the statusList, len
        """
        
        # get the len and compare it wiht len(statuses)
        self.assertEqual(len(self.mock_status_list.statuses),
                          len(self.mock_status_list))
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_argument_being_empty_string(self):
        """testing if a ValueError will be raised when the target_entity_type
        argument is given as None
        """
        
        self.kwargs["target_entity_type"] = ""
        self.assertRaises(ValueError, StatusList, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_argument_being_None(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is given as None
        """
        
        self.kwargs["target_entity_type"] = None
        self.assertRaises(TypeError, StatusList, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_attribute_is_read_only(self):
        """testing if a AttributeError will be raised when the
        target_entity_type argment is tried to be set
        """
        
        # try to set the target_entity_type attribute and expect AttributeError
        self.assertRaises(
            AttributeError,
            setattr,
            self.mock_status_list,
            "target_entity_type",
            "Sequence"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_plural_name(self):
        """testing the plural name of Status class
        """
        
        self.assertTrue(Status.plural_name, "Statuses")
    
    
    