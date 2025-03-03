import re
import pandas as pd
from datetime import datetime
def preprocess(data):
    import re
    from datetime import datetime
    import pandas as pd

    # Use raw strings for regex patterns
    pattern='\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[AP]M\s-\s'

    # Split messages and extract dates
    messages_raw = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Convert date strings to datetime objects
    date_times = [datetime.strptime(date.strip(" -"), "%m/%d/%y, %I:%M %p") for date in dates]
    df = pd.DataFrame({'raw_message': messages_raw, 'message_date': date_times})

    # Rename for clarity (optional: adjust or remove if not needed)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    parsed_messages = []  # Renamed variable to avoid conflict

    # Use a raw string in the regex for splitting user and message
    for message in df['raw_message']:
        entry = re.split(r"^([^:]+):\s(.+)$", message)
        # Check if the regex captured groups for user and message
        if len(entry) > 1:
            users.append(entry[1])
            parsed_messages.append(" ".join(entry[2:]))
        else:
            users.append('group notification')
            parsed_messages.append(entry[0])

    df['user'] = users
    df['message'] = parsed_messages
    df.drop(columns=['raw_message'], inplace=True)

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