
def dengue_desc(symptoms, per):
    symptoms_list = ''
    s_count, t_count = 0, 0
    for symp in symptoms:
        if symptoms[symp] > 0 and symp != 'days':
            symptoms_list += symp + ", "
            s_count += 1
        t_count += 1
    symptoms_list = symptoms_list[:-1]
    symptoms_list = f'You face {s_count} symptoms out of total {t_count} recognized symptoms of dengue which are ' \
                    f'{symptoms_list}. '
    report = ''
    if per >= 75:
        report += 'According to our system you have very high chances of having dengue. ' \
                  'You must consult your nearby healthcare institue or doctor as soon as possible and take steps' \
                  'according to he/she says. '
    elif 50 <= per < 75:
        report += 'According to our system you have chances of having dengue. No need to fear or panic a lot. Please consult your nearby healthcare institue or doctor as soon as possible for proper reports and testsand take steps according to he/she says. '
    elif 35 <= per < 50:
        report += 'According to our system you have low chances of having dengue. No need to fear or panic a lot. You are looking fine with less effective symptoms of dengue. But if you are not feeling well then please consult your nearby healthcare institue or ' \
                  'doctor as soon as possible for proper reports and testsand take steps according to he/she says. '
    else:
        report += 'According to our system you are safe from dengue. You are looking fine with less ' \
                  'effective symptoms of dengue. You might have a normal flue so no need to have high tensisons ' \
                  'just follow the these instructions to be safe from dengue: '
        report += symptoms_list
        report += f'According to our system you have {per}% chances of being affected of dengue. '
        report += 'Keep your environment clean around yourself and make sure your water storage area is clean.'
        return report
    report += symptoms_list
    report += f'According to our system you have {per}% chances of being affected of dengue. '
    return report
