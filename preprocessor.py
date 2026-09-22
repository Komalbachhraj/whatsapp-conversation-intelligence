# import re
# import pandas as pd
#
# def preprocess(data):
#     pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
#
#     messages = re.split(pattern, data)[1:]
#     dates = re.findall(pattern, data)
#
#     df = pd.DataFrame({'user_message': messages, 'message_date': dates})
#     # convert message_date type
#     df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
#
#     df.rename(columns={'message_date': 'date'}, inplace=True)
#
#     users = []
#     messages = []
#     for message in df['user_message']:
#         entry = re.split('([\w\W]+?):\s', message)
#         if entry[1:]:  # user name
#             users.append(entry[1])
#             messages.append(" ".join(entry[2:]))
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])
#
#     df['user'] = users
#     df['message'] = messages
#     df.drop(columns=['user_message'], inplace=True)
#
#     df['only_date'] = df['date'].dt.date
#     df['year'] = df['date'].dt.year
#     df['month_num'] = df['date'].dt.month
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['day_name'] = df['date'].dt.day_name()
#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute
#
#     period = []
#     for hour in df[['day_name', 'hour']]['hour']:
#         if hour == 23:
#             period.append(str(hour) + "-" + str('00'))
#         elif hour == 0:
#             period.append(str('00') + "-" + str(hour + 1))
#         else:
#             period.append(str(hour) + "-" + str(hour + 1))
#
#     df['period'] = period
#
#     return df


import re
import pandas as pd


def preprocess(data):

    # Remove invisible characters
    data = data.replace('\ufeff', '')
    data = data.replace('\u200e', '')
    data = data.replace('\u200f', '')

    # Normalize line endings
    data = data.replace('\r\n', '\n')
    data = data.replace('\r', '\n')

    # =========================================================
    # WHATSAPP TIMESTAMP
    #
    # Examples supported:
    #
    # 17/09/26, 10:30 - Name: Hello
    # 17/09/2026, 10:30 - Name: Hello
    # 17/09/26, 10:30 PM - Name: Hello
    # 17/09/26, 10:30:20 - Name: Hello
    # [17/09/26, 10:30:20] Name: Hello
    # 17-09-26, 10:30 - Name: Hello
    # 17.09.26, 10:30 - Name: Hello
    # =========================================================

    pattern = re.compile(
        r'(?m)^.*?'
        r'(?P<date>\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4})'
        r'\s*,\s*'
        r'(?P<time>'
        r'\d{1,2}:\d{2}'
        r'(?:[:]\d{2})?'
        r'(?:\s*[AaPp][Mm])?'
        r')'
        r'(?:\s*-\s*|\s+)'
    )

    matches = list(pattern.finditer(data))

    # =========================================================
    # DEBUG
    # =========================================================

    print("Characters in file:", len(data))
    print("Timestamp matches:", len(matches))

    # =========================================================
    # No messages found
    # =========================================================

    if len(matches) == 0:

        print("NO WHATSAPP MESSAGES DETECTED")

        return pd.DataFrame(
            columns=[
                'date',
                'user',
                'message',
                'only_date',
                'year',
                'month_num',
                'month',
                'day',
                'day_name',
                'hour',
                'minute',
                'period'
            ]
        )

    records = []

    # =========================================================
    # Extract messages
    # =========================================================

    for i, match in enumerate(matches):

        date_part = match.group('date')
        time_part = match.group('time')

        timestamp = date_part + ', ' + time_part

        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(data)

        message_text = data[start:end].strip()

        # Handle multiline messages
        message_text = re.sub(
            r'\s*\n\s*',
            ' ',
            message_text
        ).strip()

        # =====================================================
        # Extract user and message
        # =====================================================

        user_match = re.match(
            r'^([^:\n]+):\s*(.*)$',
            message_text,
            re.DOTALL
        )

        if user_match:

            user = user_match.group(1).strip()
            message = user_match.group(2).strip()

        else:

            user = 'group_notification'
            message = message_text

        records.append({
            'date': timestamp,
            'user': user,
            'message': message
        })

    # =========================================================
    # Create DataFrame
    # =========================================================

    df = pd.DataFrame(records)

    # =========================================================
    # Convert date
    # =========================================================

    df['date'] = pd.to_datetime(
        df['date'],
        dayfirst=True,
        errors='coerce'
    )

    # Remove invalid dates
    df = df.dropna(
        subset=['date']
    ).reset_index(drop=True)

    # =========================================================
    # Date information
    # =========================================================

    df['only_date'] = df['date'].dt.date

    df['year'] = df['date'].dt.year

    df['month_num'] = df['date'].dt.month

    df['month'] = df['date'].dt.month_name()

    df['day'] = df['date'].dt.day

    df['day_name'] = df['date'].dt.day_name()

    df['hour'] = df['date'].dt.hour

    df['minute'] = df['date'].dt.minute

    # =========================================================
    # Period
    # =========================================================

    period = []

    for hour in df['hour']:

        if hour == 23:
            period.append('23-00')
        else:
            period.append(
                str(hour) + '-' + str(hour + 1)
            )

    df['period'] = period

    return df