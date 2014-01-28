# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import tempfile
import unittest2
import datetime

from stalker import db
from stalker import (Task, Project, User, Status, StatusList, Repository,
                     Structure, Review)


class ReviewTestCase(unittest2.TestCase):
    """tests the stalker.models.review.Review class
    """

    def setUp(self):
        """set up the test
        """
        db.setup()
        db.init()

        self.user1 = User(
            name='Test User 1',
            login='test_user1',
            email='test1@user.com',
            password='secret'
        )
        db.session.add(self.user1)

        self.user2 = User(
            name='Test User 2',
            login='test_user2',
            email='test2@user.com',
            password='secret'
        )
        db.session.add(self.user2)

        self.user3 = User(
            name='Test User 2',
            login='test_user3',
            email='test3@user.com',
            password='secret'
        )
        db.session.add(self.user3)

        # Review Statuses
        self.status_new = Status.query.filter_by(code='NEW').first()
        self.status_rrev = Status.query.filter_by(code='RREV').first()
        self.status_app = Status.query.filter_by(code='APP').first()

        # Task Statuses
        self.status_wfd = Status.query.filter_by(code='WFD').first()
        self.status_rts = Status.query.filter_by(code='RTS').first()
        self.status_wip = Status.query.filter_by(code='WIP').first()
        self.status_prev = Status.query.filter_by(code='PREV').first()
        self.status_hrev = Status.query.filter_by(code='HREV').first()
        self.status_drev = Status.query.filter_by(code='DREV').first()
        self.status_cmpl = Status.query.filter_by(code='CMPL').first()

        self.project_status_list = StatusList(
            target_entity_type='Project',
            statuses=[
                self.status_new, self.status_wip, self.status_cmpl
            ]
        )
        db.session.add(self.project_status_list)

        self.temp_path = tempfile.mkdtemp()
        self.repo = Repository(
            name='Test Repository',
            linux_path=self.temp_path,
            windows_path=self.temp_path,
            osx_path=self.temp_path
        )
        db.session.add(self.repo)

        self.structure = Structure(
            name='Test Project Structure'
        )
        db.session.add(self.structure)

        self.project = Project(
            name='Test Project',
            code='TP',
            lead=self.user1,
            status_list=self.project_status_list,
            repository=self.repo
        )
        db.session.add(self.project)

        self.task1 = Task(
            name='Test Task 1',
            project=self.project,
            resources=[self.user1]
        )
        db.session.add(self.task1)

        self.task2 = Task(
            name='Test Task 2',
            project=self.project
        )
        db.session.add(self.task2)

        self.task3 = Task(
            name='Test Task 3',
            parent=self.task2,
            resources=[self.user1]
        )
        db.session.add(self.task3)

        self.kwargs = {
            'task': self.task1,
            'reviewer': self.user1
        }
        #self.review = Review(**self.kwargs)
        #db.session.add(self.review)

        # add everything to the db
        db.session.commit()

    def tearDown(self):
        """clean up test
        """
        db.session.close()

    def test_task_argument_is_skipped(self):
        """testing if a TypeError will be raised when the task argument is
        skipped
        """
        self.kwargs.pop('task')
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_task_argument_is_None(self):
        """testing if a TypeError will be raised when the task argument is None
        """
        self.kwargs['task'] = None
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_task_argument_is_not_a_Task_instance(self):
        """testing if a TypeError will be raised when the task argument value
        is not a Task instance
        """
        self.kwargs['task'] = 'not a Task instance'
        self.assertRaises(TypeError, Review, **self.kwargs)

    # def test_task_attribute_is_read_only(self):
    #     """testing if a the task attribute is read only
    #     """
    #     now = datetime.datetime.now()
    #     self.task1.create_time_log(
    #         resource=self.task1.resources[0],
    #         start=now,
    #         end=now + datetime.timedelta(hours=1)
    #     )
    #     reviews = self.task1.request_review()
    #     review = reviews[0]
    #     self.assertRaises(AttributeError, setattr, review, 'task', self.task1)

    def test_task_argument_is_not_a_leaf_task(self):
        """testing if a ValueError will be raised when the task given in task
        argument is not a leaf task
        """
        task1 = Task(
            name='Task1',
            project=self.project
        )
        task2 = Task(
            name='Task2',
            parent=task1
        )
        self.kwargs['task'] = task1
        self.assertRaises(ValueError, Review, **self.kwargs)

    def test_task_argument_is_working_properly(self):
        """testing if the task argument value is passed to the task argument
        properly
        """
        now = datetime.datetime.now()
        self.task1.create_time_log(
            resource=self.task1.resources[0],
            start=now,
            end=now + datetime.timedelta(hours=1)
        )
        reviews = self.task1.request_review()
        self.assertEqual(reviews[0].task, self.task1)

    def test_auto_name_is_true(self):
        """testing if review instances are named automatically
        """
        self.assertTrue(Review.__auto_name__)

    def test_status_is_new_for_a_newly_created_review_instance(self):
        """testing if the status is NEW for a newly created review instance
        """
        review = Review(**self.kwargs)
        self.assertEqual(review.status, self.status_new)

    def test_review_number_attribute_is_a_read_only_attribute(self):
        """testing if the review_number attribute is a read only attribute
        """
        review = Review(**self.kwargs)
        self.assertRaises(
            AttributeError, setattr, review, 'review_number', 2
        )

    def test_review_number_attribute_is_initialized_to_the_task_review_number_plus_1(self):
        """testing if the review_number attribute is initialized with
        task.review_number + 1
        """
        review = Review(**self.kwargs)
        self.assertEqual(1, review.review_number)

    def test_review_number_for_multiple_responsible_task_is_equal_to_each_other(self):
        """testing if the review.review_number attribute for each review
        instance created for a task with multiple responsible are equal to each
        other
        """
        self.task1.responsible = [self.user1, self.user2, self.user3]
        now = datetime.datetime.now()
        self.task1.create_time_log(
            resource=self.task1.resources[0],
            start=now,
            end=now + datetime.timedelta(hours=1)
        )
        reviews = self.task1.request_review()
        expected_review_number = self.task1.review_number + 1

        self.assertEqual(3, len(reviews))

        self.assertEqual(
            expected_review_number,
            reviews[0].review_number
        )

        self.assertEqual(
            expected_review_number,
            reviews[1].review_number
        )

        self.assertEqual(
            expected_review_number,
            reviews[2].review_number
        )

    def test_reviewer_argument_is_skipped(self):
        """testing if a TypeError will be raised when the reviewer argument is
        skipped
        """
        self.kwargs.pop('reviewer')
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_reviewer_argument_is_None(self):
        """testing if a TypeError will be raised when the reviewer argument is
        None
        """
        self.kwargs['reviewer'] = None
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_reviewer_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the reviewer attribute is
        set to None
        """
        review = Review(**self.kwargs)
        self.assertRaises(TypeError, setattr, review, 'reviewer', None)

    def test_reviewer_argument_is_not_a_User_instance(self):
        """testing if a TeypeError will be raised when the reviewer argument is
        not a User instance
        """
        self.kwargs['reviewer'] = 'not a user instance'
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_reviewer_attribute_is_not_a_User_instance(self):
        """testing if a TypeError will be raised when the reviewer attribute is
        set to a value other than a User instance
        """
        review = Review(**self.kwargs)
        self.assertRaises(TypeError, setattr, review, 'reviewer', 'not a user')

    def test_reviewer_argument_is_not_in_Task_responsible_list(self):
        """testing if it is possible to use some other user which is not in the
        Task.responsible list as the reviewer
        """
        self.task1.responsible = [self.user1]
        self.kwargs['reviewer'] = self.user2
        review = Review(**self.kwargs)
        self.assertEqual(review.reviewer, self.user2)

    def test_reviewer_attribute_is_not_in_Task_responsible_list(self):
        """testing if it is possible to use some other user which is not in the
        Task.responsible list as the reviewer
        """
        self.task1.responsible = [self.user1]
        self.kwargs['reviewer'] = self.user1
        review = Review(**self.kwargs)
        review.reviewer = self.user2
        self.assertEqual(review.reviewer, self.user2)

    def test_reviewer_argument_is_working_properly(self):
        """testing if the reviewer argument value is correctly passed to
        reviewer attribute
        """
        self.task1.responsible = [self.user1]
        self.kwargs['reviewer'] = self.user1
        review = Review(**self.kwargs)
        self.assertEqual(
            self.user1,
            review.reviewer
        )

    def test_reviewer_attribute_is_working_properly(self):
        """testing if the reviewer attribute is working properly
        """
        self.task1.responsible = [self.user1, self.user2]
        self.kwargs['reviewer'] = self.user1
        review = Review(**self.kwargs)
        review.reviewer = self.user2
        self.assertEqual(
            self.user2,
            review.reviewer
        )

    # TODO: think about adding tests for the same user is being the reviewer for
    #       multiple reviews with same level with same task

    def test_approve_method_updates_task_status_correctly_for_a_single_responsible_task(self):
        """testing if the Review.approve() method will update the task status
        correctly for a task with only one responsible
        """
        self.task1.responsible = [self.user1]
        self.kwargs['reviewer'] = self.user1
        self.assertNotEqual(
            self.status_cmpl,
            self.task1.status
        )
        review = Review(**self.kwargs)
        review.approve()
        self.assertEqual(
            self.status_cmpl,
            self.task1.status
        )

    def test_approve_method_updates_task_status_correctly_for_a_multi_responsible_task_when_all_approve(self):
        """testing if the Review.approve() method will update the task status
        correctly for a task with multiple responsible
        """
        self.task1.responsible = [self.user1, self.user2]

        now = datetime.datetime.now()
        self.task1.create_time_log(
            resource=self.user1,
            start=now,
            end=now + datetime.timedelta(hours=1)
        )

        reviews = self.task1.request_review()
        review1 = reviews[0]
        review2 = reviews[1]

        review1.approve()
        # still pending review
        self.assertEqual(
            self.status_prev,
            self.task1.status
        )

        # first reviewer
        review2.approve()
        self.assertEqual(
            self.status_cmpl,
            self.task1.status
        )

    def test_approve_method_updates_task_parent_status(self):
        """testing if approve method will also update the task parent status
        """
        self.task3.status = self.status_rts
        now = datetime.datetime.now()
        td = datetime.timedelta
        self.task3.create_time_log(
            resource=self.task3.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        reviews = self.task3.request_review()
        self.assertEqual(
            self.task3.status, self.status_prev
        )

        review1 = reviews[0]
        review1.approve()

        self.assertEqual(
            self.task3.status, self.status_cmpl
        )

        self.assertEqual(
            self.task2.status, self.status_cmpl
        )

    def test_approve_method_updates_task_status_correctly_for_a_multi_responsible_task_when_one_approve(self):
        """testing if the Review.approve() method will update the task status
        correctly for a task with multiple responsible
        """
        self.task1.responsible = [self.user1, self.user2]
        now = datetime.datetime.now()
        td = datetime.timedelta
        self.task1.create_time_log(
            resource=self.task1.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        reviews = self.task1.request_review()
        review1 = reviews[0]
        review2 = reviews[1]

        review1.request_revision()
        # one requst review should be enough to set the status to hrev,
        # note that this is another tests duty to check
        self.assertEqual(
            self.status_prev,
            self.task1.status
        )

        # first reviewer
        review2.approve()
        self.assertEqual(
            self.status_hrev,
            self.task1.status
        )

    def test_request_revision_method_updates_task_status_correctly_for_a_single_responsible_task(self):
        """testing if the Review.request_revision() method will update the task
        status correctly to HREV for a Task with only one responsible
        """
        self.task1.responsible = [self.user1]
        now = datetime.datetime.now()
        self.task1.create_time_log(
            resource=self.task1.resources[0],
            start=now,
            end=now + datetime.timedelta(hours=1)
        )

        reviews = self.task1.request_review()
        review = reviews[0]
        review.request_revision()
        self.assertEqual(
            self.status_hrev,
            self.task1.status
        )

    def test_request_revision_method_updates_task_status_correctly_for_a_multi_responsible_task_when_one_request_revision(self):
        """testing if the Review.request_revision() method will update the
        task status correctly for a Task with multiple responsible
        """
        self.task1.responsible = [self.user1, self.user2]
        now = datetime.datetime.now()
        self.task1.create_time_log(
            resource=self.task1.resources[0],
            start=now,
            end=now + datetime.timedelta(hours=1)
        )

        # first reviewer requests a revision
        reviews = self.task1.request_review()

        review1 = reviews[0]
        review2 = reviews[1]

        review1.approve()
        self.assertEqual(
            self.status_prev,
            self.task1.status
        )

        review2.request_revision()
        self.assertEqual(
            self.status_hrev,
            self.task1.status
        )

    def test_request_revision_method_updates_task_status_correctly_for_a_multi_responsible_task_when_all_request_revision(self):
        """testing if the Review.request_revision() method will update the
        task status correctly for a Task with multiple responsible
        """
        self.task1.responsible = [self.user1, self.user2]
        now = datetime.datetime.now()
        self.task1.create_time_log(
            resource=self.task1.resources[0],
            start=now,
            end=now + datetime.timedelta(hours=1)
        )

        # first reviewer requests a revision
        reviews = self.task1.request_review()

        review1 = reviews[0]
        review2 = reviews[1]

        review1.request_revision()
        self.assertEqual(
            self.status_prev,
            self.task1.status
        )

        # first reviewer
        review2.request_revision()
        self.assertEqual(
            self.status_hrev,
            self.task1.status
        )

    def test_request_revision_method_updates_task_timing_correctly_for_a_multi_responsible_task_when_all_request_revision(self):
        """testing if the Review.request_revision() method will update the task
        timing values correctly for a Task with multiple responsible
        """
        self.task1.responsible = [self.user1, self.user2]
        self.assertEqual(
            self.status_rts,
            self.task1.status
        )
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()
        # create 1 hour time log
        self.task1.create_time_log(
            resource=self.user1,
            start=now,
            end=now + td(hours=1)
        )

        # first reviewer requests a revision
        reviews = self.task1.request_review()

        self.assertEqual(len(reviews), 2)

        review1 = reviews[0]
        review2 = reviews[1]

        review1.request_revision(
            schedule_timing=2,
            schedule_unit='h',
            description='do some 2 hours extra work'
        )
        self.assertEqual(
            self.status_prev,
            self.task1.status
        )

        # first reviewer
        review2.request_revision(
            schedule_timing=5,
            schedule_unit='h',
            description='do some 5 hours extra work'
        )

        self.assertEqual(
            self.status_hrev,
            self.task1.status
        )

        # check the timing values
        self.assertEqual(self.task1.schedule_timing, 8)
        self.assertEqual(self.task1.schedule_unit, 'h')

    def test_review_set_property_return_all_the_revision_instances_with_same_review_number(self):
        """testing if review_set property returns all the Review instances of
        the same task with the same review_number
        """
        self.task1.responsible = [self.user1, self.user2, self.user3]
        now = datetime.datetime.now()
        self.task1.create_time_log(
            resource=self.user1,
            start=now,
            end=now + datetime.timedelta(hours=1)
        )
        self.task1.status = self.status_wip
        reviews = self.task1.request_review()
        review1 = reviews[0]
        review2 = reviews[1]
        review3 = reviews[2]

        self.assertEqual(review1.review_number, 1)
        self.assertEqual(review2.review_number, 1)
        self.assertEqual(review3.review_number, 1)
        self.task1.approve()

        review4 = self.task1.request_revision(reviewer=self.user1)

        self.task1.status = self.status_wip
        self.assertEqual(review4.review_number, 2)

        # enter new time log to turn it into WIP
        self.task1.create_time_log(
            resource=self.user1,
            start=now + datetime.timedelta(hours=1),
            end=now + datetime.timedelta(hours=2)
        )

        review_set2 = self.task1.request_review()
        review5 = review_set2[0]
        review6 = review_set2[1]
        review7 = review_set2[2]

        self.assertEqual(review5.review_number, 3)
        self.assertEqual(review6.review_number, 3)
        self.assertEqual(review7.review_number, 3)