import unittest
from unittest.mock import Mock
from glm53_api import GLM53API, GLMAPIError
class T(unittest.TestCase):
 def s(self,status=200,p=None):
  s=Mock(); r=Mock(status_code=status); r.json.return_value=p or {'choices':[]}; s.post.return_value=r; return s
 def test_payload(self):
  s=self.s(); GLM53API('k',session=s).chat([{'role':'user','content':'x'}]); self.assertEqual(s.post.call_args.kwargs['json']['model'],'glm-5.3')
 def test_rejects_none(self):
  with self.assertRaises(GLMAPIError): GLM53API('k',session=self.s()).chat([{'role':'user','content':'x'}],reasoning_effort='none')
if __name__=='__main__': unittest.main()
