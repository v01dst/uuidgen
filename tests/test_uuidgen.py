import unittest
import os
import sys
import uuid
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from uuidgen import cmd_gen, cmd_parse, cmd_validate


class TestGen(unittest.TestCase):
    def test_v4(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_gen(type("A", (), {"version": 4, "count": 3, "namespace": None, "name": None})())
        lines = buf.getvalue().strip().splitlines()
        self.assertEqual(len(lines), 3)
        for l in lines:
            u = uuid.UUID(l)
            self.assertEqual(u.version, 4)

    def test_v1(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_gen(type("A", (), {"version": 1, "count": 1, "namespace": None, "name": None})())
        u = uuid.UUID(buf.getvalue().strip())
        self.assertEqual(u.version, 1)

    def test_v7(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_gen(type("A", (), {"version": 7, "count": 1, "namespace": None, "name": None})())
        u = uuid.UUID(buf.getvalue().strip())
        self.assertEqual(u.version, 7)


class TestParse(unittest.TestCase):
    def test_parse(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_parse(type("A", (), {"uuid": "550e8400-e29b-41d4-a716-446655440000"})())
        out = buf.getvalue()
        self.assertIn("version: 4", out)
        self.assertIn("variant: specified in RFC 4122", out)


class TestValidate(unittest.TestCase):
    def test_valid(self):
        import io
        from contextlib import redirect_stdout, redirect_stderr
        buf = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(err):
            try:
                cmd_validate(type("A", (), {"uuid": "550e8400-e29b-41d4-a716-446655440000"})())
            except SystemExit:
                pass
        self.assertIn("valid", buf.getvalue())

    def test_invalid(self):
        import io
        from contextlib import redirect_stdout, redirect_stderr
        buf = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(err):
            try:
                cmd_validate(type("A", (), {"uuid": "not-a-uuid"})())
            except SystemExit:
                pass
        self.assertIn("invalid", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
