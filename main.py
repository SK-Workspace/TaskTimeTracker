from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # Read the CSV file, specifying comma as the delimiter
        data = pd.read_csv(file, header=None, skiprows=1)

        # Split the single column into multiple columns
        data = data[0].str.split(',', expand=True)

        # Rename the columns
        data.columns = ['timestamp', 'userID', 'taskID', 'eventType']

        # Strip leading/trailing whitespaces from each cell
        data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        # Convert 'timestamp' column to integers and 'eventType' column to strings
        data['timestamp'] = pd.to_datetime(data['timestamp'].astype(int), unit='s')
        data['eventType'] = data['eventType'].astype(str)

        # Sort the data by timestamp
        data = data.sort_values('timestamp')

        # Initialize an empty dictionary to store the start time of tasks
        start_time = {}

        # Initialize an empty dictionary to store the total time spent on each task by each user
        total_time = {}

        # Initialize an empty list to store discrepancies
        discrepancies = []

        # Iterate over each row in the DataFrame
        for index, row in data.iterrows():
            # Check if all necessary fields are present in the row
            if row['userID'] and row['taskID'] and row['eventType'] and row['timestamp']:
                # Create a tuple to represent the user and task
                user_task = (row['userID'], row['taskID'])
                # Check the event type
                if row['eventType'] == 'Task Started':
                    # If the task has already been started, log a discrepancy
                    if user_task in start_time:
                        discrepancies.append(f'{user_task[0]} {user_task[1]} {row['timestamp']} Discrepancy: Task {user_task[1]} was started again without being stopped or completed by user {user_task[0]}. Current started entry will be ignored and first entry will be considered.')
                    else:
                        # Record the start time of the task
                        start_time[user_task] = row['timestamp']
                elif row['eventType'] in ['Task Stopped', 'Task Completed']:
                    # If the task was not started, log a discrepancy
                    if user_task not in start_time:
                        discrepancies.append(f'{user_task[0]} {user_task[1]} {row['timestamp']} Discrepancy: Task {user_task[1]} was stopped or completed without being started by user {user_task[0]}. Current stopped or completed entry will be ignored.')
                    else:
                        # Calculate the time spent on the task
                        time_spent = row['timestamp'] - start_time[user_task]
                        # Add the time spent to the total time for the task
                        if user_task in total_time:
                            total_time[user_task] += time_spent
                        else:
                            total_time[user_task] = time_spent
                        # Remove the task from the start time dictionary as time_spent has been calculated
                        del start_time[user_task]
                else:
                    # If the event type is not recognized, log a discrepancy
                    discrepancies.append(f'{row['userID']} {row['taskID']} {row['timestamp']} Discrepancy: New eventType:{row['eventType']} found for userID:{row['userID']} and taskID:{row['taskID']}')
            else:
                # If any necessary field is missing, log a discrepancy
                discrepancies.append(f'{row['userID'] if row['userID'] else '-' } {row['taskID'] if row['taskID'] else '-' } {row['timestamp'] if row['timestamp'] else '-' } Discrepancy: No data found in one or more columns (UserID, taskID, timestamp, eventType)')

        # Check if start_time dictionary has data and add them to discrepancies as missing stopped or completed event
        if start_time:
            for key,value in start_time.items():
                discrepancies.append(f'{key[0]} {key[1]} {value} Discrepancy: No stopped or completed event found for userID:{key[0]} and taskID:{key[1]} after the started event')

        # Prepare the report
        report = {
            'total_time': {f'User {k[0]} Task {k[1]}': str(v) for k, v in total_time.items()},
            'discrepancies': discrepancies
        }
        # Render the report in the report.html template
        return render_template('report.html', report=report)
    # Render the upload form in the upload.html template
    return render_template('report.html',report=None)

if __name__ == '__main__':
    app.run(debug=True)
