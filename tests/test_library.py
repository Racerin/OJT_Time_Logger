import os
import tempfile
import unittest

import library

class TestLibrary(unittest.TestCase):
    
    def test_get_db(self):
        """Test 'get_db' function."""
        _, filename = tempfile.mkstemp()
        # Create database connection
        conn = library.get_db(filename)
        # Test connnection attributes
        self.assertIsInstance(conn, library.sqlite3.Connection)
        self.assertIs(conn.row_factory, library.sqlite3.Row)
        # Test bad inputs
        err_inputs = (
            ([],TypeError),
            (1,TypeError),
            ('',ValueError),
        )
        for err_input, err in err_inputs:
            with self.assertRaises(err, msg=err_input):
                library.get_db(err_input)

    def test_is_email(self):
        """Test for 'is_email' function."""
        # Legit emails
        emails = [
            "d@g.com",
            "foobar@example.com",
            "foobar@example.org",
            "foo.bar@example.com",
            "foo@exam.ple.edu",
            "foo.bar@axam.ple.org"
        ]
        for email in emails:
            ans = library.is_email(email)
            self.assertIsInstance(ans, bool, msg=email)
            self.assertTrue(ans, msg=email)
        # Illegitimate emails
        not_emails = [
            "foobar",
            "@example.com",
            "foobar@example",
            ".@example.com",
            "x"*100 + "@game",
        ]
        for email in not_emails:
            ans  = library.is_email(email)
            self.assertIsInstance(ans, bool, msg=email)
            self.assertFalse(ans, msg=email)
        # Errors
        error_inputs = [
            1,
            [],
            ['a','b'],
            b'foo',
            None,
        ]
        for error_input in error_inputs:
            with self.assertRaises(TypeError, msg=error_input):
                library.is_email(error_input)
        

    def test_salt_password(self):
        """Test 'salt_password' function."""
        salt = "fish"
        passwords = [
            'apple',
            '1',
            '11',
            "x"*100,
            b'a'
        ]
        for pw in passwords:
            ans = library.salt_password(pw, salt, iterations=2)
            # Returns a byte
            self.assertIsInstance(ans, bytes, msg=pw)
            # Input doesn NOT equal output
            b_password = pw if isinstance(pw, bytes) else pw.encode()  #ensure its in bytes
            self.assertNotEqual(ans, b_password, msg=pw)
        # Errors
        error_inputs = [
            1,
            [],
            '',
            None,
        ]
        for error_input in error_inputs:
            with self.assertRaises((TypeError, AttributeError, ValueError), msg=error_input):
                library.salt_password(error_input, salt, iterations=2)


    def test_is_password(self):
        """Test the 'is_password' function. 
        I don't know why the function exists.
        """
        pass


    def test_has_digit(self):
        """Test the 'has_digit' function. """
        # Test valids
        contains_digit = [
            '1',
            '11',
            '10.5',
            'alpha 1',
            '1 alpha',
            'dog2dog',
            '1love',
            'love2'
        ]
        for stri in contains_digit:
            ans = library.has_digit(stri)
            self.assertIsInstance(ans, bool, msg=stri)
            self.assertTrue(ans, msg=stri)
        # Test invalids
        contains_no_digits = [
            '',
            'a',
            'aaaa',
            '!@#$',
            'Foo Bar',
        ]
        for stri in contains_no_digits:
            ans = library.has_digit(stri)
            self.assertIsInstance(ans, bool, msg=stri)
            self.assertFalse(ans, msg=stri)
        # Test Errors
        error_inputs = [
            1,
            b'foo',
            b"123",
            [],
            ['1', '2', ],
            None,
        ]
        for error_input in error_inputs:
            with self.assertRaises((TypeError, AttributeError), msg=error_input):
                library.has_digit(error_input)


    def test_has_letter(self):
        """Test the 'has_letter' function. """
        # Test valids
        contains_letter = [
            "l",
            "2l",
            "32109f",
            "()*3213290g",
        ]
        for stri in contains_letter:
            ans = library.has_letter(stri)
            self.assertIsInstance(ans, bool, msg=stri)
            self.assertTrue(ans, msg=stri)
        # Test invalids
        contains_no_letters = [
            "2",
            "!@#$()(*31123",
            "0980959082",
            "",
        ]
        for stri in contains_no_letters:
            ans = library.has_letter(stri)
            self.assertIsInstance(ans, bool, msg=stri)
            self.assertFalse(ans, msg=stri)
        # Test Errors
        error_inputs = [
            1,
            b'foo',
            b"123",
            [],
            None,
        ]
        for error_input in error_inputs:
            with self.assertRaises((TypeError, AttributeError, ), msg=error_input):
                library.has_letter(error_input)


    def test_has_symbol(self):
        """Test the 'has_symbol' function. """
        # Test valids
        contains_symbol = [
            '1@',
            '11!',
            '10.5',
            'alpha 1(',
        ]
        for stri in contains_symbol:
            ans = library.has_symbol(stri)
            self.assertIsInstance(ans, bool, msg=stri)
            self.assertTrue(ans, msg=stri)
        # Test invalids
        contains_no_symbols = [
            '',
            'a',
            'aaaa',
            '21312',
            'Foo Bar',
        ]
        for stri in contains_no_symbols:
            ans = library.has_symbol(stri)
            self.assertIsInstance(ans, bool, msg=stri)
            self.assertFalse(ans, msg=stri)
        # Test Errors
        error_inputs = [
            1,
            b'foo',
            [],
            None,
        ]
        for error_input in error_inputs:
            with self.assertRaises((TypeError, AttributeError), msg=error_input):
                library.has_symbol(error_input)

    def test_has_whitespace(self):
        """Test the 'has_whitespace' function. """
        # Test valids
        contains_whitespace = [
            '11 !',
            'Foo Bar'
            'alpha 1(',
            'Bert ',
            ' AlphaLion'
        ]
        for stri in contains_whitespace:
            ans = library.has_whitespace(stri)
            self.assertIsInstance(ans, bool, msg=stri)
            self.assertTrue(ans, msg=stri)
        # Test invalids
        contains_no_whitespaces = [
            '',
            'a',
            'aaaa',
            '21312',
            'FooBar',
        ]
        for stri in contains_no_whitespaces:
            ans = library.has_whitespace(stri)
            self.assertIsInstance(ans, bool, msg=stri)
            self.assertFalse(ans, msg=stri)
        # Test Errors
        error_inputs = [
            1,
            b'foo',
            [],
            None,
        ]
        for error_input in error_inputs:
            with self.assertRaises((TypeError, AttributeError), msg=error_input):
                library.has_whitespace(error_input)

    def test_del_file(self):
        """Test the 'del_file' function."""
        # Create file
        _, filename = tempfile.mkstemp()
        with open(filename, mode='+w'):
            pass
        # Test existence
        assert os.path.exists(filename), "The file should exists."
        # Delete File
        library.del_file(filename)
        # Test inexistence
        assert not os.path.exists(filename), "The file should not exist."
        # Test non-existence
        library.del_file(filename)