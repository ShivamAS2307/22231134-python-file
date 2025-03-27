import pandas as pd
data_1 = {
    'student_id': [101, 101, 101, 101, 101, 102, 102, 102, 102, 103, 103, 103, 103, 103, 104, 104, 104, 104, 104],
    'attendance_date': ['2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05',
                        '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05',
                        '2024-03-05', '2024-03-06', '2024-03-07', '2024-03-08', '2024-03-09',
                        '2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05'],
    'status': ['Absent', 'Absent', 'Absent', 'Absent', 'Present',
               'Absent', 'Absent', 'Absent', 'Absent',
               'Absent', 'Absent', 'Absent', 'Absent', 'Absent',
               'Present', 'Present', 'Absent', 'Present', 'Present']
}
dataframe1 = pd.DataFrame(data_1)
dataframe1['attendance_date'] = pd.to_datetime(dataframe1['attendance_date'])

def locate_streaks(df):
    output_data = []
    for studentNumber, dataBlock in df.groupby('student_id'):
        dataBlock = dataBlock.sort_values('attendance_date')
        countOfAbsences = 0
        beginningDate = None
        for idx, record in dataBlock.iterrows():
            if record['status'] == 'Absent':
                if beginningDate is None:
                    beginningDate = record['attendance_date']
                countOfAbsences += 1
            else:
                if countOfAbsences >= 3:
                    end_date = record['attendance_date'] - pd.Timedelta(days=1)
                    output_data.append([studentNumber, beginningDate, end_date, countOfAbsences])
                countOfAbsences = 0
                beginningDate = None
        if countOfAbsences >= 3:
            output_data.append([studentNumber, beginningDate, dataBlock['attendance_date'].iloc[-1], countOfAbsences])

    result_df = pd.DataFrame(output_data, columns=['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days'])
    return result_df

absence_data = locate_streaks(dataframe1)
student_info = {
    'student_id': [101, 102, 103, 104, 105],
    'student_name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'David Lee', 'Eva White'],
    'parent_email': ['alice_parent@example.com', 'bob_parent@example.com', 'invalid_email.com', 'invalid_email.com', 'eva_white@example.com']
}

students_data = pd.DataFrame(student_info)
combinedData = []
for _, absence_row in absence_data.iterrows():
    matchingRow = students_data[students_data['student_id'] == absence_row['student_id']]
    if not matchingRow.empty:
        combinedRow = {
            **absence_row,
            **matchingRow.iloc[0]
        }
        combinedData.append(combinedRow)
combinedDataFrame = pd.DataFrame(combinedData)

def emailValidator(email_address):
    if not isinstance(email_address, str):
        return False
    if '@' not in email_address or '.' not in email_address:
        return False
    if email_address.count('@') != 1:
        return False
    return True
combinedDataFrame['valid_email'] = combinedDataFrame['parent_email'].apply(emailValidator)

def generateParentMessage(row):
    if row['valid_email']:
        msg = f"Dear Parent, your child {row['student_name']} was absent from {row['absence_start_date'].date()} to {row['absence_end_date'].date()} for {row['total_absent_days']} days. Please ensure their attendance improves."
        return msg
    else:
        return None
combinedDataFrame['parent_message'] = combinedDataFrame.apply(generateParentMessage, axis=1)
pd.set_option('display.max_colwidth', None)
print(combinedDataFrame)
