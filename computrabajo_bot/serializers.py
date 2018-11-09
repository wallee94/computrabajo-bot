from rest_framework import serializers as ser


class ComputrabajoSerializer(ser.Serializer):
    state_choices = [
        "ciudad-de-mexico",
        "aguascalientes",
        "baja-california",
        "baja-california-sur",
        "campeche",
        "coahuila-de-zaragoza",
        "colima",
        "chiapas",
        "chihuahua",
        "durango",
        "guanajuato",
        "guerrero",
        "hidalgo",
        "jalisco",
        "estado-de-mexico",
        "michoacan-de-ocampo",
        "morelos",
        "nayarit",
        "nuevo-leon",
        "oaxaca",
        "puebla",
        "queretaro",
        "quintana-roo",
        "san-luis-potosi",
        "sinaloa",
        "sonora",
        "tabasco",
        "tamaulipas",
        "tlaxcala",
        "veracruz-de-ignacio-de-la-llave",
        "yucatan",
        "zacatecas",
        "jornada-desde-casa",
    ]
    pub_choices = [7, 15, 30]
    salary_choices = [n for n in range(1, 7)]

    username = ser.EmailField(max_length=200)
    password = ser.CharField(max_length=150)
    query = ser.CharField(max_length=150, required=False, allow_null=True)
    state = ser.ChoiceField(choices=state_choices, required=False, allow_null=True)
    pub = ser.ChoiceField(choices=pub_choices, required=False, allow_null=True)
    salary = ser.ChoiceField(choices=salary_choices, required=False, allow_null=True)
