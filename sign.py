import requests

urlist = ["http://api.turinglabs.net/api/v1/jd/ddfactory/create/P04z54XCjVWnYaS5nFATA-LhQ/",
"http://api.turinglabs.net/api/v1/jd/jxfactory/create/SJofod7WOWvvv9i8dqOw7g==/",
"http://api.turinglabs.net/api/v1/jd/bean/create/zbtt6vjy2eppryhor7gxqk7dxe/",
"http://api.turinglabs.net/api/v1/jd/bean/create/olmijoxgmjutzmd7pdefkvkpvzih4mhujntklla/",
"http://api.turinglabs.net/api/v1/jd/bean/create/e7lhibzb3zek3z335qojblyednxc7ifyfim5wbi/",
"http://api.turinglabs.net/api/v1/jd/farm/create/0df62cce371f4999a7f633a781726123/",
"http://api.turinglabs.net/api/v1/jd/farm/create/6c892c16c708490a8194ac685c54a7e2/",
"http://api.turinglabs.net/api/v1/jd/farm/create/0cda90d46c1f4219b677a583ea317e9e/",
"http://api.turinglabs.net/api/v1/jd/pet/create/MTE1NDAxNzgwMDAwMDAwMzYyNjQxMjM=/",
"http://api.turinglabs.net/api/v1/jd/pet/create/MTAxODEyMjkxMDAwMDAwMDQwMTMwNjQ5/"]


for i in urlist:
    data = requests.get(i)
