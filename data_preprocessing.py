import pandas as pd
import re


def preprocessing(content):
    regex = r'\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s?[ap]m\s-\s'

    if re.split(regex, content)[0] == "":
        messages = re.split(regex, content)[1:]
    else:
        messages = re.split(regex, content)[0:]
    dates = re.findall(regex, content)

    print(len(messages), len(dates))

    df = pd.DataFrame({"user_messages": messages, "message_date": dates})
    df["message_date"] = pd.to_datetime(df["message_date"], format="%d/%m/%Y, %I:%M %p - ")
    df.rename(columns={"message_date": "date"}, inplace=True)
    df.head()

    users = []
    messages = []
    for message in df["user_messages"]:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:] and entry[1:][1] != "<Media omitted>\n":
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])

    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user_messages"], inplace=True)
    df["message"] = df["message"].apply(lambda x: x[:-1])

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df


def preprocessing2(content):
    regex = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s?[apAP][mM]\s-\s'

    if re.split(regex, content)[0] == "":
        messages = re.split(regex, content)[1:]
    else:
        messages = re.split(regex, content)[0:]
    dates = re.findall(regex, content)

    df = pd.DataFrame({"user_messages": messages, "message_date": dates})

    df["message_date"] = pd.to_datetime(df["message_date"], format="%m/%d/%y, %I:%M %p - ")
    df.rename(columns={"message_date": "date"}, inplace=True)
    df.head()

    # In[46]:

    users = []
    messages = []
    for message in df["user_messages"]:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:] and entry[1:][1] != "<Media omitted>\n":
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])

    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user_messages"], inplace=True)
    df["message"] = df["message"].apply(lambda x: x[:-1])

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
