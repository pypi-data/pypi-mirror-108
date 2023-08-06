from melaxtool.melaxapi import MelaxClient

if __name__ == '__main__':
    import os

    # copy your key  to set env below
    os.environ[
        'MELAX_TECH_KEY'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIxIiwidXJsIjoiaHR0cHM6Ly9tZXJjdXJ5LWRldi5tZWxheHRlY2guY29tIn0.tyKkNMRt4inVUWyriKl5knPF5kOEa3lYKT07bDTFVV8"

    input = """
    Admission Date:  [**2118-6-2**]       Discharge Date:  [**2118-6-14**]

Date of Birth:                    Sex:  F

Service:  MICU and then to [**Doctor Last Name **] Medicine

HISTORY OF PRESENT ILLNESS:  This is an 81-year-old female
with a history of emphysema (not on home O2), who presents
with three days of shortness of breath thought by her primary
care doctor to be a COPD flare.  Two days prior to admission,
she was started on a prednisone taper and one day prior to
admission she required oxygen at home in order to maintain
oxygen saturation greater than 90%.  She has also been on
levofloxacin and nebulizers, and was not getting better, and
presented to the [**Hospital1 18**] Emergency Room.
"""

client = MelaxClient('/Users/lvjian/key.txt')

response = client.visualization(input, "clinical:4")



# print(len(response.getAllSentence()))


# print(len(response.getAllSentence()))
