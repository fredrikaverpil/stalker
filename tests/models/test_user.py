# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause


import unittest
import datetime
from stalker import db
from stalker.conf import defaults
from stalker.db.session import DBSession, ZopeTransactionExtension
from stalker import (Group, Department, Project, Repository,
                     Sequence, Status, StatusList, Task, Type, User, Version, Ticket)

class UserTest(unittest.TestCase):
    """Tests the user class
    """
    
    @classmethod
    def setUpClass(cls):
        """set up the test for class
        """
        DBSession.remove()
        DBSession.configure(extension=None)
    
    @classmethod
    def tearDownClass(cls):
        """clean up the test
        """
        DBSession.configure(extension=ZopeTransactionExtension())
    
    def setUp(self):
        """setup the test
        """
        
        # setup a test database
        self.TEST_DATABASE_URI = "sqlite:///:memory:"
        db.setup()
        
        # need to have some test object for
        # a department
        self.test_department1 = Department(
            name="Test Department 1"
        )
        self.test_department2 = Department(
            name="Test Department 2"
        )
        self.test_department3 = Department(
            name="Test Department 3"
        )
        
        DBSession.add_all([
            self.test_department1,
            self.test_department2,
            self.test_department3
        ])
        
        # a couple of groups
        self.test_group1 = Group(
            name="Test Group 1"
        )
        self.test_group2 = Group(
            name="Test Group 2"
        )
        self.test_group3 = Group(
            name="Test Group 3"
        )
        
        DBSession.add_all([
            self.test_group1,
            self.test_group2,
            self.test_group3
        ])

        # a couple of statuses
        self.test_status1 = Status(name="Completed", code="CMPLT")
        self.test_status2 = Status(name="Work In Progress", code="WIP")
        self.test_status3 = Status(name="Waiting To Start", code="WTS")
        self.test_status4 = Status(name="Pending Review", code="PRev")
        
        DBSession.add_all([
            self.test_status1,
            self.test_status2,
            self.test_status3,
            self.test_status4
        ])
        
        # a project status list
        self.project_status_list = StatusList(
            name="Project Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4
            ],
            target_entity_type=Project,
        )
        
        # a repository type
        self.test_repository_type = Type(
            name="Test",
            code='test',
            target_entity_type=Repository,
        )
        
        # a repository
        self.test_repository = Repository(
            name="Test Repository",
            type=self.test_repository_type
        )

        # a project type
        self.commercial_project_type = Type(
            name="Commercial Project",
            code='comm',
            target_entity_type=Project,
        )
        
        # a couple of projects
        self.test_project1 = Project(
            name="Test Project 1",
            code='tp1',
            status_list=self.project_status_list,
            type=self.commercial_project_type,
            repository=self.test_repository,
        )
        
        self.test_project2 = Project(
            name="Test Project 2",
            code='tp2',
            status_list=self.project_status_list,
            type=self.commercial_project_type,
            repository=self.test_repository,
        )

        self.test_project3 = Project(
            name="Test Project 3",
            code='tp3',
            status_list=self.project_status_list,
            type=self.commercial_project_type,
            repository=self.test_repository,
        )
        
        DBSession.add_all([
            self.test_project1,
            self.test_project2,
            self.test_project3
        ])
        
        # a task status list
        self.task_status_list = StatusList(
            name="Task Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4
            ],
            target_entity_type=Task
        )

        # a couple of tasks
        self.test_task1 = Task(
            name="Test Task 1",
            status_list=self.task_status_list,
            project=self.test_project1,
            task_of=self.test_project1
        )

        self.test_task2 = Task(
            name="Test Task 2",
            status_list=self.task_status_list,
            project=self.test_project1,
            task_of=self.test_project1
        )

        self.test_task3 = Task(
            name="Test Task 3",
            status_list=self.task_status_list,
            project=self.test_project2,
            task_of=self.test_project1
        )

        self.test_task4 = Task(
            name="Test Task 4",
            status_list=self.task_status_list,
            project=self.test_project3,
            task_of=self.test_project1
        )
        
        DBSession.add_all([
            self.test_task1,
            self.test_task2,
            self.test_task3,
            self.test_task4
        ])
        
        # a couple of versions
        # a version status list
        self.version_status_list = StatusList(
            name="Version Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4
            ],
            target_entity_type=Version
        )
        
        # for task1
        self.test_version1 = Version(
            version_of=self.test_task1,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version1)
        
        self.test_version2 = Version(
            version_of=self.test_task1,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version2)
        
        self.test_version3 = Version(
            version_of=self.test_task1,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version3)
        
        # for task2
        self.test_version4 = Version(
            version_of=self.test_task2,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version4)
        
        self.test_version5 = Version(
            version_of=self.test_task2,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version5)
        
        self.test_version6 = Version(
            version_of=self.test_task2,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version6)
        
        # for task3
        self.test_version7 = Version(
            version_of=self.test_task3,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version7)
        
        self.test_version8 = Version(
            version_of=self.test_task3,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version8)
        
        self.test_version9 = Version(
            version_of=self.test_task3,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version9)
        
        # for task4
        self.test_version10 = Version(
            version_of=self.test_task4,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version10)
        
        self.test_version11 = Version(
            version_of=self.test_task4,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version11)
        
        self.test_version12 = Version(
            version_of=self.test_task4,
            status_list=self.version_status_list
        )
        DBSession.add(self.test_version12)
        
        # *********************************************************************
        # Tickets
        # *********************************************************************
        
        # no need to create status list for tickets cause we have a database
        # set up an running so it will be automatically linked
        
        # tickets for version1
        self.test_ticket1 = Ticket(
            ticket_for=self.test_version1,
        )
        DBSession.add(self.test_ticket1)
        # set it to closed
        self.test_ticket1.resolve()
        
        # create a new ticket and leave it open
        self.test_ticket2 = Ticket(
            ticket_for=self.test_version1,
        )
        DBSession.add(self.test_ticket2)
        
        # create a new ticket and close and then reopen it
        self.test_ticket3 = Ticket(
            ticket_for=self.test_version1,
        )
        DBSession.add(self.test_ticket3)
        self.test_ticket3.resolve()
        self.test_ticket3.reopen()
        
        # *********************************************************************
        # tickets for version2
        # create a new ticket and leave it open
        self.test_ticket4 = Ticket(
            ticket_for=self.test_version2,
        )
        DBSession.add(self.test_ticket4)
        
        # create a new Ticket and close it
        self.test_ticket5 = Ticket(
            ticket_for=self.test_version2,
        )
        DBSession.add(self.test_ticket5)
        self.test_ticket5.resolve()
        
        # create a new Ticket and close it
        self.test_ticket6 = Ticket(
            ticket_for=self.test_version3,
        )
        DBSession.add(self.test_ticket6)
        self.test_ticket6.resolve()
        
        # *********************************************************************
        # tickets for version3
        # create a new ticket and close it
        self.test_ticket7 = Ticket(
            ticket_for=self.test_version3,
        )
        DBSession.add(self.test_ticket7)
        self.test_ticket7.resolve()
        
        # create a new ticket and close it
        self.test_ticket8 = Ticket(
            ticket_for=self.test_version3,
        )
        DBSession.add(self.test_ticket8)
        self.test_ticket8.resolve()
        
        # *********************************************************************
        # tickets for version4
        # create a new ticket and close it
        self.test_ticket9 = Ticket(
            ticket_for=self.test_version4,
        )
        DBSession.add(self.test_ticket9)
        self.test_ticket9.resolve()
        
        # no tickets for any other version
        # *********************************************************************
        
        # a status list for sequence
        self.sequence_status_list = StatusList(
            name="Sequence Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4
            ],
            target_entity_type=Sequence
        )

        # a couple of sequences
        self.test_sequence1 = Sequence(
            name="Test Seq 1",
            code='ts1',
            project=self.test_project1,
            status_list=self.sequence_status_list
        )

        self.test_sequence2 = Sequence(
            name="Test Seq 2",
            code='ts2',
            project=self.test_project1,
            status_list=self.sequence_status_list
        )

        self.test_sequence3 = Sequence(
            name="Test Seq 3",
            code='ts3',
            project=self.test_project1,
            status_list=self.sequence_status_list
        )

        self.test_sequence4 = Sequence(
            name="Test Seq 4",
            code='ts4',
            project=self.test_project1,
            status_list=self.sequence_status_list
        )
        
        DBSession.add_all([
            self.test_sequence1,
            self.test_sequence2,
            self.test_sequence3,
            self.test_sequence4
        ])

        # a test admin
        #self.test_admin = User(
        #    name='Admin',
        #    login='admin',
        #    email='admin@admin.com',
        #    password='admin'
        #)
        self.test_admin = User.query.filter_by(name=defaults.ADMIN_NAME)\
                                                                       .first()
        self.assertIsNotNone(self.test_admin)
        
        # create the default values for parameters
        self.kwargs = {
            'name': 'Erkan Ozgur Yilmaz',
            'login': 'eoyilmaz',
            'description': 'this is a test user',
            'password': 'hidden',
            'email': 'eoyilmaz@fake.com',
            'department': self.test_department1,
            'groups': [self.test_group1,
                       self.test_group2],
            'projects_lead': [self.test_project1,
                              self.test_project2],
            'sequences_lead': [self.test_sequence1,
                               self.test_sequence2,
                               self.test_sequence3,
                               self.test_sequence4],
            'created_by': self.test_admin,
            'updated_by': self.test_admin,
            'last_login': None
        }
        
        # create a proper user object
        self.test_user = User(**self.kwargs)
        DBSession.add(self.test_user)
        DBSession.commit()
        
        # just change the kwargs for other tests
        self.kwargs['name'] = 'some other name'
        self.kwargs['email'] = 'some@other.email'
    
    def tearDown(self):
        """tear down the test
        """
        DBSession.remove()
    
    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        User class
        """
        self.assertFalse(User.__auto_name__)
     
    def test_email_argument_accepting_only_string_or_unicode(self):
        """testing if email argument accepting only string or unicode
        values
        """
        # try to create a new user with wrong attribute
        test_values = [1, 1.3, ["an email"], {"an": "email"}]

        for test_value in test_values:
            self.kwargs["email"] = test_value
            self.assertRaises(TypeError, User, **self.kwargs)

    def test_email_attribute_accepting_only_string_or_unicode(self):
        """testing if email attribute accepting only string or unicode
        values
        """
        # try to assign something else than a string or unicode
        test_value = 1

        self.assertRaises(
            TypeError,
            setattr,
            self.test_user,
            "email",
            test_value
        )

        test_value = ["an email"]

        self.assertRaises(
            TypeError,
            setattr,
            self.test_user,
            "email",
            test_value
        )

    def test_email_argument_format(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        test_values = ["an email in no format",
                       "an_email_with_no_part2",
                       "@an_email_with_only_part2",
                       "@",
                       ]
        # any of this values should raise a ValueError
        for test_value in test_values:
            self.kwargs["email"] = test_value
            self.assertRaises(ValueError, User, **self.kwargs)

    def test_email_attribute_format(self):
        """testing if given an email in wrong format will raise a ValueError 
        """
        test_values = [
            "an email in no format",
            "an_email_with_no_part2",
            "@an_email_with_only_part2",
            "@",
            "eoyilmaz@",
            "eoyilmaz@somecompony@com",
        ]
        # any of these email values should raise a ValueError
        for value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.test_user,
                "email",
                value
            )

    def test_email_attribute_works_properly(self):
        """testing if email attribute works properly
        """
        test_email = "eoyilmaz@somemail.com"
        self.test_user.email = test_email
        self.assertEqual(self.test_user.email, test_email)

    def test_login_argument_conversion_to_strings(self):
        """testing if a ValueError will be raised when the given objects
        conversion to string results an empty string
        """
        test_values = ["----++==#@#$", ]
        for test_value in test_values:
            self.kwargs["login"] = test_value
            self.assertRaises(ValueError, User, **self.kwargs)

    def test_login_argument_for_empty_string(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to login argument
        """
        self.kwargs["login"] = ""
        self.assertRaises(ValueError, User, **self.kwargs)

    def test_login_attribute_for_empty_string(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to login attribute
        """
        self.assertRaises(
            ValueError,
            setattr,
            self.test_user,
            "login",
            ""
        )

    def test_login_argument_is_skipped(self):
        """testing if a TypeError will be raised when the login argument is
        skipped
        """
        self.kwargs.pop("login")
        self.assertRaises(TypeError, User, **self.kwargs)
    
    def test_login_argument_is_None(self):
        """testing if a TypeError will be raised when trying to assign None
        to login argument
        """
        self.kwargs["login"] = None
        self.assertRaises(TypeError, User, **self.kwargs)

    def test_login_attribute_is_None(self):
        """testing if a TypeError will be raised when trying to assign None
        to login attribute
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_user,
            "login",
            None
        )
    
    def test_login_argument_formatted_correctly(self):
        """testing if login argument formatted correctly
        """
        #                 input       expected
        test_values = [("e. ozgur", "eozgur"),
            ("erkan", "erkan"),
            ("Ozgur", "ozgur"),
            ("Erkan ozgur", "erkanozgur"),
            ("eRKAN", "erkan"),
            ("eRkaN", "erkan"),
            (" eRkAn", "erkan"),
            (" eRkan ozGur", "erkanozgur"),
            ("213 e.ozgur", "eozgur"),
        ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            self.kwargs["login"] = valuePair[0]
            test_user = User(**self.kwargs)
            self.assertEqual(
                test_user.login,
                valuePair[1]
            )

    def test_login_attribute_formatted_correctly(self):
        """testing if login attribute formatted correctly
        """
        #                 input       expected
        test_values = [("e. ozgur", "eozgur"),
            ("erkan", "erkan"),
            ("Ozgur", "ozgur"),
            ("Erkan ozgur", "erkanozgur"),
            ("eRKAN", "erkan"),
            ("eRkaN", "erkan"),
            (" eRkAn", "erkan"),
            (" eRkan ozGur", "erkanozgur"),
        ]

        for valuePair in test_values:
            # set the input and expect the expected output
            self.test_user.login = valuePair[0]

            self.assertEqual(
                self.test_user.login,
                valuePair[1]
            )
    
    def test_login_argument_is_working_properly(self):
        """testing if the login argument is working properly
        """
        self.assertEqual(self.test_user.login, self.kwargs['login'])
    
    def test_login_attribute_is_working_properly(self):
        """testing if the login attribute is working properly
        """
        test_value = 'newlogin'
        self.test_user.login = test_value
        self.assertEqual(self.test_user.login, test_value)
    
    def test_last_login_argument_accepts_None(self):
        """testing if nothing happens when the last login argument is set to
        None
        """
        self.kwargs["last_login"] = None
        # nothing should happen
        a_new_user = User(**self.kwargs)

    def test_last_login_attribute_None(self):
        """testing if nothing happens when the last login attribute is set to
        None
        """
        # nothing should happen
        self.test_user.last_login = None

    def test_last_login_argument_accepts_datetime_instance(self):
        """testing if a nothing happens when tried to set the last_login
        to a datetime.datetime instance
        """
        self.kwargs["last_login"] = datetime.datetime.now()
        # nothing should happen
        a_new_user = User(**self.kwargs)

    def test_last_login_argument_accepts_only_datetime_instance_or_None(self):
        """testing if a TypeError will be raised for values other than a
        datetime.datetime instances or None tried to be set to last_login
        argument
        """
        test_values = [1, 2.3, "login time", ["last login time"],
                {"a last": "login time"}]
        for test_value in test_values:
            self.kwargs["last_login"] = test_value
            self.assertRaises(TypeError, User, **self.kwargs)

    def test_last_login_attribute_accepts_only_datetime_instance_or_None(self):
        """testing if a TypeError will be raised for values other than
        datetime.datetime instances tried to be assigned to last_login
        attribute
        """
        test_values = [1, 2.3, "login time", ["last login time"],
                {"a last": "login time"}]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_user,
                "last_login",
                test_value
            )

    def test_last_login_attribute_works_properly(self):
        """testing if the last_login attribute works properly
        """
        test_value = datetime.datetime.now()
        self.test_user.last_login = test_value
        self.assertEqual(self.test_user.last_login, test_value)
    
    def test_departments_argument_is_skipped(self):
        """testing if a User can be created without a Department instance
        """
        try:
            self.kwargs.pop('departments')
        except KeyError:
            pass
        
        new_user = User(**self.kwargs)
        self.assertEqual(new_user.departments, [])
    
    def test_departments_argument_is_None(self):
        """testing if a User can be created with the departments argument value
        is to None
        """
        self.kwargs['departments'] = None
        new_user = User(**self.kwargs)
        self.assertEqual(new_user.departments, [])
    
    def test_departments_attribute_is_set_None(self):
        """testing if a TypeError will be raised when the User's departments
        attribute set to None
        """
        self.assertRaises(TypeError, setattr, self.test_user, 'departments',
                          None)
    
    def test_departments_argument_is_an_empty_list(self):
        """testing if a User can be created with the departments argument is an
        empty list
        """
        self.kwargs['departments'] = []
        new_user = User(**self.kwargs)
    
    def test_departments_attribute_is_an_empty_list(self):
        """testing if the departments attribute can be set to an empty list
        """
        self.test_user.departments = []
        self.assertEqual(self.test_user.departments, [])
    
    def test_departments_argument_only_accepts_list_of_department_objects(self):
        """testing if a TypeError will be raised when trying to assign
        anything other than a Department object to departments argument
        """
        # try to assign something other than a department object
        test_values = [
            "A department",
            1,
            1.0,
            ["a department"],
            {"a": "deparment"}
        ]
        
        self.kwargs["departments"] = test_values
        self.assertRaises(TypeError, User, **self.kwargs)
    
    def test_departments_attribute_only_accepts_department_objects(self):
        """testing if a TypeError will be raised when trying to assign
        anything other than a Department object to departments attribute
        """
        # try to assign something other than a department
        test_value = "a department"
        self.assertRaises(
            TypeError,
            setattr,
            self.test_user,
            "departments",
            test_value
        )

    def test_departments_attribute_works_properly(self):
        """testing if departments attribute works properly
        """
        # try to set and get the same value back
        self.test_user.departments = [self.test_department2]
        self.assertItemsEqual(self.test_user.departments, [self.test_department2])
    
    def test_departments_attribute_supports_appending(self):
        """testing if departments attribute supports appending
        """
        self.test_user.departments = []
        self.test_user.departments.append(self.test_department1)
        self.test_user.departments.append(self.test_department2)
        self.assertItemsEqual(self.test_user.departments,
                              [self.test_department1, self.test_department2])
    
    def test_password_argument_being_None(self):
        """testing if a TypeError will be raised when trying to assign None
        to the password argument
        """
        self.kwargs["password"] = None
        self.assertRaises(TypeError, User, **self.kwargs)

    def test_password_attribute_being_None(self):
        """testing if a TypeError will be raised when tyring to assign None to
        the password attribute
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_user,
            "password",
            None
        )

    def test_password_attribute_works_properly(self):
        """testing if password attribute works properly
        """
        test_password = "a new test password"
        self.test_user.password = test_password
        self.assertNotEquals(self.test_user.password, test_password)

    def test_password_argument_being_scrambled(self):
        """testing if password is scrambled when trying to store it
        """
        test_password = "a new test password"
        self.kwargs["password"] = test_password
        aNew_user = User(**self.kwargs)
        self.assertNotEquals(aNew_user.password, test_password)

    def test_password_attribute_being_scrambled(self):
        """testing if password is scrambled when trying to store it
        """
        test_password = "a new test password"
        self.test_user.password = test_password
        
        # test if they are not the same any more
        self.assertNotEquals(self.test_user.password, test_password)

    def test_check_password_works_properly(self):
        """testing if check_password method works properly
        """
        test_password = "a new test password"
        self.test_user.password = test_password

        # check if it is scrambled
        self.assertNotEquals(self.test_user.password, test_password)

        # check if check_password returns True
        self.assertTrue(self.test_user.check_password(test_password))

        # check if check_password returns False
        self.assertFalse(self.test_user.check_password("wrong pass"))

    def test_groups_argument_for_None(self):
        """testing if the groups attribute will be an empty list
        when the groups argument is None
        """
        self.kwargs["groups"] = None
        new_user = User(**self.kwargs)
        self.assertEqual(new_user.groups, [])

    def test_groups_attribute_for_None(self):
        """testing if a TypeError will be raised when groups attribute is set
        to None
        """
        self.assertRaises(TypeError, setattr, self.test_user, "groups", None)

    def test_groups_argument_accepts_only_Group_instances(self):
        """testing if a TypeError will be raised when trying to assign anything
        other then a Group instances to the group argument
        """
        test_values = [
            23123,
            1231.43122,
            "a_group",
            ["group1", "group2", 234],
        ]

        for test_value in test_values:
            self.kwargs["groups"] = test_value
            self.assertRaises(TypeError, User, **self.kwargs)

    def test_groups_attribute_accepts_only_Group_instances(self):
        """testing if a TypeError will be raised when trying to assign anything
        other then a Group instances to the group attribute
        """
        test_values = [
            23123,
            1231.43122,
            "a_group",
            ["group1", "group2", 234],
        ]

        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_user,
                "groups",
                test_value
            )

    def test_groups_attribute_works_properly(self):
        """testing if groups attribute works properly
        """
        test_pg = [self.test_group3]
        self.test_user.groups = test_pg
        self.assertEqual(self.test_user.groups, test_pg)

    def test_groups_attribute_elements_accepts_Group_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Group instances to the groups list
        """
        # append
        self.assertRaises(
            TypeError,
            self.test_user.groups.append,
            0
        )

        # __setitem__
        self.assertRaises(
            TypeError,
            self.test_user.groups.__setitem__,
            0,
            0
        )

    def test_projects_attribute_is_read_only(self):
        """testing if the project attribute is read-only
        """
        self.assertRaises(AttributeError, setattr, self.test_user, "projects",
            [])

    def test_projects_attribute_is_calculated_from_the_tasks_attribute(self):
        """testing if the projects is gathered from the tasks attribute
        directly
        """
        # create a new project
        commercial_project_type = Type(
            name="Commercial Project",
            code='comm',
            target_entity_type=Project
        )

        complete_status = Status(name="Complete", code="CMPL")
        wip_status = Status(name="Work In Progress", code="WIP")

        project_status_list = StatusList(
            name="Project Status List",
            statuses=[wip_status, complete_status],
            target_entity_type="Project"
        )

        new_project1 = Project(
            name="New Project 1",
            code='np1',
            type=commercial_project_type,
            status_list=project_status_list,
            repository=self.test_repository,
            )

        new_project2 = Project(
            name="New Project 2",
            code='np2',
            type=commercial_project_type,
            status_list=project_status_list,
            repository=self.test_repository,
            )

        task_status_list = StatusList(
            name="Task Status List",
            statuses=[wip_status, complete_status],
            target_entity_type="Task"
        )

        # create a new user
        new_user = User(
            name='Erkan Ozgur Yilmaz',
            login='eoyilmaz',
            email='eoyilmaz@fake.com',
            password='hidden'
        )

        # create a couple of tasks
        design_task_type = Type(
            name="Design",
            code='design',
            target_entity_type=Task
        )

        modeling_task_type = Type(
            name="Modeling",
            code='modeling',
            target_entity_type=Task
        )

        shading_task_type = Type(
            name="Shading",
            code='shading',
            target_entity_type=Task
        )

        task1 = Task(
            name="Modeling",
            resources=[new_user],
            type=modeling_task_type,
            status_list=task_status_list,
            task_of=new_project1,
            )

        task2 = Task(
            name="Shading",
            resources=[new_user],
            type=shading_task_type,
            status_list=task_status_list,
            task_of=new_project1,
            )

        task3 = Task(
            name="Design",
            resources=[new_user],
            type=design_task_type,
            status_list=task_status_list,
            task_of=new_project2,
            )

        # now check the user.projects
        #print new_user.projects
        #print task1.project
        #print task2.project
        #print task3.project

        self.assertItemsEqual(new_user.projects, [new_project1, new_project2])

    #def test_projects_attribute_is_calculated_from_the_asset_tasks(self):
        #"""testing if the projects is gathered from the asset tasks
        #"""

        #self.fail("test is not implemented yet")

    #def test_projects_attribute_is_calculated_from_the_sequence_tasks(self):
        #"""testing if the projects is gathered from the sequence tasks
        #"""

        #self.fail("test is not implemented yet")
    
    #def test_projects_attribute_is_calculated_from_the_shot_tasks(self):
        #"""testing if the projects is gathered from the shot tasks
        #"""
        #self.fail("test is not implemented yet")

    def test_projects_lead_argument_None(self):
        """testing if the projects_lead attribute will be an empty list when
        the projects_lead attribute is None
        """
        self.kwargs["projects_lead"] = None
        new_user = User(**self.kwargs)
        self.assertEqual(new_user.projects_lead, [])

    def test_projects_lead_attribute_None(self):
        """testing if a TypeError will be raised when the project_lead
        attribute is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_user, "projects_lead",
                          None)

    def test_projects_lead_argument_accepts_empty_list(self):
        """testing if projects_lead argument accepts an empty list
        """
        self.kwargs["projects_lead"] = []
        # this should work without any problems
        self.test_user = User(**self.kwargs)

    def test_projects_lead_attribute_accepts_empty_list(self):
        """testing if projects_lead attribute accepts an empty list
        """

        # this should work without any problem
        self.test_user.projects_lead = []


    def test_projects_lead_argument_accepts_only_list(self):
        """testing if a TypeError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        projects_lead argument
        """
        test_values = ["a project", 123123, {}, 12.2132]
        for test_value in test_values:
            self.kwargs["projects_lead"] = test_value
            self.assertRaises(TypeError, User, **self.kwargs)

    def test_projects_lead_argument_accepts_only_lists_of_project_obj(self):
        """testing if a TypeError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        projects_lead argument
        """
        test_value = ["a project", 123123, [], {}, 12.2132]
        self.kwargs["projects_lead"] = test_value
        self.assertRaises(TypeError, User, **self.kwargs)

    def test_projects_lead_attribute_accepts_only_lists(self):
        """testing if a TypeError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        projects_lead attribute
        """
        test_values = ["a project", 123123, {}, 12.2132]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_user,
                "projects_lead",
                test_value
            )

    def test_projects_lead_attribute_accepts_only_list_of_project_obj(self):
        """testing if a TypeError will be raised when trying to assign a list
        of other object than a list of Project objects to the
        projects_lead attribute
        """
        test_value = ["a project", 123123, [], {}, 12.2132]
        self.assertRaises(
            TypeError,
            setattr,
            self.test_user,
            "projects_lead",
            test_value
        )

    def test_projects_lead_attribute_working_properly(self):
        """testing if the projects_lead attribute is working properly
        """
        projects_lead = [self.test_project1,
                         self.test_project2,
                         self.test_project3]
        self.test_user.projects_lead = projects_lead
        self.assertEqual(self.test_user.projects_lead, projects_lead)

    def test_projects_lead_attribute_elements_accepts_Project_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Project object to the projects_lead list
        """
        # append
        self.assertRaises(
            TypeError,
            self.test_user.projects_lead.append,
            0
        )

        # __setitem__
        self.assertRaises(
            TypeError,
            self.test_user.projects_lead.__setitem__,
            0,
            0
        )

    def test_sequences_lead_argument_None(self):
        """testing if the sequences_lead attribute will be an empty list when
        the sequences_lead argument is None
        """
        self.kwargs["sequences_lead"] = None
        new_user = User(**self.kwargs)
        self.assertEqual(new_user.sequences_lead, [])

    def test_sequences_lead_attribute_None(self):
        """testing if a TypeError will be raised when the sequences_lead
        attribute is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_user, "sequences_lead",
                          None)

    def test_sequences_lead_argument_accepts_empty_list(self):
        """testing if sequences_lead argument accepts an empty list
        """
        self.kwargs["sequences_lead"] = []
        #this should work
        a_user = User(**self.kwargs)

    def test_sequences_lead_attribute_accepts_empty_list(self):
        """testing if sequences_lead attribute accepts an empty list
        """
        # this should work without any error
        self.test_user.sequences_lead = []

    def test_sequences_lead_argument_accepts_only_lists(self):
        """testing if a TypeError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        sequences_lead argument
        """
        test_values = ["a sequence", 123123, {}, 12.2132]
        for test_value in test_values:
            self.kwargs["sequences_lead"] = test_value
            self.assertRaises(TypeError, User, **self.kwargs)

    def test_sequences_lead_argument_accepts_only_lists_of_project_obj(self):
        """testing if a TypeError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        sequences_lead argument
        """
        test_value = ["a sequence", 123123, [], {}, 12.2132]
        self.kwargs["sequences_lead"] = test_value
        self.assertRaises(TypeError, User, **self.kwargs)

    def test_sequences_lead_attribute_accepts_only_list_of_project_obj(self):
        """testing if a TypeError will be raised when trying to assign a list
        of other object than a list of Project objects to the
        sequences_lead attribute
        """
        test_value = ["a sequence", 123123, [], {}, 12.2132]
        self.kwargs["sequences_lead"] = test_value
        self.assertRaises(TypeError, User, **self.kwargs)

    def test_sequence_lead_attribute_works_propertly(self):
        """testing if sequence_lead attribute works properly
        """
        self.assertEqual(self.test_user.sequences_lead,
                         self.kwargs["sequences_lead"]
        )

    def test_sequences_lead_attribute_elements_accepts_Project_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Sequence object to the sequence_lead list
        """
        # append
        self.assertRaises(
            TypeError,
            self.test_user.sequences_lead.append,
            0
        )

        # __setitem__
        self.assertRaises(
            TypeError,
            self.test_user.sequences_lead.__setitem__,
            0,
            0
        )

    def test_tasks_argument_None(self):
        """testing if the tasks attribute will be an empty list when the tasks
        argument is given as None
        """
        self.kwargs["tasks"] = None
        new_user = User(**self.kwargs)
        self.assertEqual(new_user.tasks, [])

    def test_tasks_attribute_None(self):
        """testing if a TypeError will be raised when the tasks attribute is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_user, "tasks", None)

    def test_tasks_argument_accepts_only_list_of_task_objects(self):
        """testing if a TypeError will be raised when trying to assign
        anything other than a list of task objects to the tasks argument
        """
        test_values = [12312, 1233244.2341, ["aTask1", "aTask2"], "a_task"]

        for test_value in test_values:
            self.kwargs["tasks"] = test_value
            self.assertRaises(TypeError, User, **self.kwargs)

    def test_tasks_attribute_accepts_only_list_of_task_objects(self):
        """testing if a TypeError will be raised when trying to assign
        anything other than a list of task objects to the tasks argument
        """
        test_values = [12312, 1233244.2341, ["aTask1", "aTask2"], "a_task"]

        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_user,
                "tasks",
                test_value
            )

    def test_tasks_argument_accepts_an_empty_list(self):
        """testing if nothing happens when trying to assign an empty list to
        tasks argument
        """
        self.kwargs["tasks"] = []

        # this should work without any error
        aUserObj = User(**self.kwargs)

    def test_tasks_attribute_accepts_an_empty_list(self):
        """testing if nothing happens when trying to assign an empty list to
        tasks attribute
        """
        # this should work without any error
        self.test_user.tasks = []

    def test_tasks_attribute_works_properly(self):
        """testing if tasks attribute is working properly
        """
        tasks = [self.test_task1,
                 self.test_task2,
                 self.test_task3,
                 self.test_task4]

        self.test_user.tasks = tasks

        self.assertEqual(self.test_user.tasks, tasks)

    def test_tasks_attribute_elements_accepts_Tasks_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Task object to the tasks list
        """
        # append
        self.assertRaises(
            TypeError,
            self.test_user.tasks.append,
            0
        )

    def test_equality_operator(self):
        """testing equality of two users
        """
        #same_user = User(**self.kwargs)
        
        self.kwargs.update({
            "name": "Generic User",
            "description": "this is a different user",
            "login": "guser",
            "email": "generic.user@generic.com",
            "password": "verysecret",
        })
        
        new_user = User(**self.kwargs)
        
        #self.assertTrue(self.test_user == same_user)
        self.assertFalse(self.test_user == new_user)

    def test_inequality_operator(self):
        """testing inequality of two users
        """
        #same_user = User(**self.kwargs)

        self.kwargs.update({
            "name": "Generic User",
            "description": "this is a different user",
            "login": "guser",
            "email": "generic.user@generic.com",
            "password": "verysecret",
            })

        new_user = User(**self.kwargs)

        #self.assertFalse(self.test_user != same_user)
        self.assertTrue(self.test_user != new_user)

#    def test_initials_argument_is_skipped(self):
#        """testing if a TypeError will be raised when the initials argument is
#        skipped
#        """
#        self.kwargs.pop('initials')
#        self.assertRaises(TypeError, User, **self.kwargs)
#    
#    def test_initials_argument_is_an_empty_string(self):
#        """testing if a ValueError will be raised when the initials argument is
#        an empty string
#        """
#        self.kwargs['initials'] = ''
#        self.assertRaises(ValueError, User, **self.kwargs)
#    
#    def test_initials_attribute_is_set_to_string(self):
#        """testing if a ValueError will be raised when the initials attribute
#        is set to an empty string
#        """
#        self.assertRaises(ValueError, setattr, self.test_user, 'initials', '')
#    
#    def test_initials_argument_is_not_a_string(self):
#        """testing if a TypeError will be raised when the initials argument is
#        not a string
#        """
#        self.kwargs['initials'] = 1
#        self.assertRaises(TypeError, User, **self.kwargs)
#    
#    def test_initials_attribute_is_not_set_to_a_string(self):
#        """testing if a TypeError will be raised when the initials attribute is
#        set to a value other than a string
#        """
#        self.assertRaises(TypeError, setattr, self.test_user, 'initials', 1)
#    
#    def test_initials_argument_working_properly(self):
#        """testing the initials argument is working properly
#        """
#        self.kwargs["initials"] = "eoy"
#        new_user = User(**self.kwargs)
#        self.assertEqual(new_user.initials, self.kwargs["initials"])
#    
#    def test_initials_attribute_is_working_properly(self):
#        """testing if initials attribute working properly
#        """
#        test_value = "eoy"
#        self.test_user.initials = test_value
#        self.assertEqual(self.test_user.initials, test_value)

    def test___repr__(self):
        """testing the representation
        """
        self.assertEqual(
            self.test_user.__repr__(),
            "<User (%s ('%s'))>" % (
                self.test_user.name,
                self.test_user.login)
        )
    
    #def test_plural_name(self):
        #"""testing the plural name of User class
        #"""

        #self.assertTrue(User.plural_name, "Users")
    
    def test_tickets_attribute_is_an_empty_list_by_default(self):
        """testing if the User.tickets is an empty list by default
        """
        self.assertEqual(self.test_user.tickets, [])
    
    def test_open_tickets_attribute_is_an_empty_list_by_default(self):
        """testing if the User.open_tickets is an empty list by default
        """
        self.assertEqual(self.test_user.open_tickets, [])
    
    def test_tickets_attribute_is_read_only(self):
        """testing if the User.tickets attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_user, 'tickets',
            [])
    
    def test_open_tickets_attribute_is_read_only(self):
        """testing if the User.open_tickets attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_user,
                          'open_tickets', [])
    
    def test_tickets_attribute_returns_all_tickets_of_versions_of_tasks_of_this_user(self):
        """testing if User.tickets returns all the tickets of versions of tasks
        of this user
        """
        self.assertEqual(len(self.test_user.tasks), 0)
        
        # there should be no tickets assigned to this user
        self.assertTrue(self.test_user.tickets == [])
        
        # assign the user as a resource for task1
        self.test_task1.resources.append(self.test_user)
        
        # now we should have some open tickets
        self.assertTrue(len(self.test_user.tickets) > 0)
        
        # now check for exact items
        self.assertItemsEqual(
            self.test_user.tickets,
            [
                # version1 tickets
                self.test_ticket1, self.test_ticket2, self.test_ticket3,
                # version2 tickets
                self.test_ticket4, self.test_ticket5, self.test_ticket6,
                # version3 tickets
                self.test_ticket7, self.test_ticket8
            ]
        )
    

    def test_open_tickets_attribute_returns_all_open_tickets_of_versions_of_tasks_of_this_user(self):
        """testing if User.open_tickets returns all the open tickets of
        versions of tasks of this user
        """
        self.assertEqual(len(self.test_user.tasks), 0)
        
        # there should be no tickets assigned to this user
        self.assertTrue(self.test_user.open_tickets == [])
        
        # assign the user as a resource for task1
        self.test_task1.resources.append(self.test_user)
        
        # now we should have some open tickets
        self.assertTrue(len(self.test_user.open_tickets) > 0)
        
        # now check for exact items
        self.assertItemsEqual(
            self.test_user.open_tickets,
            [
                # version1 tickets
                self.test_ticket2, self.test_ticket3,
                # version2 tickets
                self.test_ticket4,
            ]
        )