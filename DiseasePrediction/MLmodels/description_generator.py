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


def generate_report_description(report, disease):
    desc = ''
    if report.chances >= 75:
        desc += f'According to our system you have very high chances of having {disease}. ' \
                'You must consult your nearby healthcare institue or doctor as soon as possible and take steps' \
                'according to he/she says. '
    elif 50 <= report.chances < 75:
        desc += f'According to our system you have chances of having {disease}. ' \
                'No need to fear or panic a lot. ' \
                'Please consult your nearby healthcare institue or doctor as soon as possible for proper reports ' \
                'and testsand take steps according to he/she says. '
    elif 35 <= report.chances < 50:
        desc += f'According to our system you have low chances of having {disease}. ' \
                f'No need to fear or panic a lot. You are looking fine with less effective symptoms of {disease}. ' \
                'But if you are not feeling well then please consult your nearby healthcare institue or ' \
                'doctor as soon as possible for proper reports and testsand take steps according to he/she says. '
    else:
        desc += f'According to our system you are safe from {disease}. You are looking fine with less ' \
                f'effective symptoms of {disease}. You might have a normal flue so no need to have high tensisons '
    symptoms = report.symptoms.split(',')
    s_count = len(symptoms)
    desc += f' You face {s_count} ' \
            f'recognized symptoms of {report.type} which are {report.symptoms}. ' \
            f'According to our system you have {report.chances}% chance of being ' \
            f'affected of {report.type}. '
    return desc


def generate_result(per, disease):
    result = ""
    if per >= 75:
        result = f'Very high {disease} positive chances.'
    elif 50 <= per < 75:
        result = f'High {disease} positive chances'
    elif 35 <= per < 50:
        result = f'Low {disease} positive chances'
    else:
        result = f'Safe from {disease}'
    return result


def general_Result_Generator(res):
    desc = ''
    if int(res) == 1:
        msg = 'Normal flue'
        desc = 'You may have normal flue and if you are not feeling extremely well then consult your nearby doctor'
    elif int(res) == 2:
        msg = 'Chances of Dengue'
        desc = 'Chances of Dengue.... take proper dengue test for better results'
    elif int(res) == 3:
        msg = 'Chances of Chikungunya'
        desc = 'Chances of Chikungunya.... take proper chikungunya test for better results'
    elif int(res) == 4:
        msg = 'Chances of Malaria'
        desc = 'Chances of Malaria.... take proper malaria test for better results'
    elif int(res) == 5:
        msg = 'Chances of Covid-19'
        desc = 'Chances of Covid-19.... take proper Covid-19 test for better results'
    else:
        msg = 'Unrecognized Disease'
        desc = 'You may have serious disease please concern doctor as soon as possible'
    return msg,desc
