# Covid-19 API
![Python](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) 	![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

A Web API for getting consice and compiled imformation at a single stop about **Covid-19** cases and vaccinations in **India** in past **30 days**. The data is collected from offical **csv data** file provided by Goverenment of India, processed using **data analytic** libraries and hosted on **pythonanywhere**

**API Documentation** `http://peter316.pythonanywhere.com/`

### Endpoints**

------------
![Endpoints](https://github.com/Shivam-316/Covid-19_API/blob/b0f9e649a2a6a4f8459e49b23527ee11f6540e4a/markdownImages/endpoints.png?raw=true)

### Acessing Data**

------------

**Base URL:** `http://peter316.pythonanywhere.com/api/v1`

The `{region}` has to be replaced with **key** which is state code for each state in India.
**keys** can be accessed using the endpoint `/regions/info` along with **Base URL**
```json
[
  {
    "state": "India",
    "key": "IND"
  },
  {
    "state": "Andaman and Nicobar Islands",
    "key": "AN"
  },
]
```

Also, you can use the **Swagger Documentation** to see working of different Endpoints.

![Swagger Doc. Endpoint](https://github.com/Shivam-316/Covid-19_API/blob/841f38b6aba23d2a0062afb8c5bcf2de234dab18/markdownImages/Sdoc%20endpoint.png?raw=true)


	** Subject to updation in version v2.
