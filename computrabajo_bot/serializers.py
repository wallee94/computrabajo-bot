from rest_framework import serializers as ser


class ComputrabajoSerializer(ser.Serializer):
    state_choices = []
    pub_choices = [7, 15, 30]
    salary_choices = [n for n in range(1, 7)]

    username = ser.EmailField(max_length=200)
    password = ser.CharField(max_length=150)
    query = ser.CharField(max_length=150, required=False)
    state = ser.ChoiceField(choices=state_choices, required=False)
    pub = ser.ChoiceField(choices=pub_choices, required=False)
    salary = ser.ChoiceField(choices=salary_choices, required=False)