<h1>Task Time Tracker</h1>

<h2>Overview</h2>

<p>This is a Flask application that reads a CSV file uploaded by the user and generates a report. The CSV file should contain event logs with the following columns: timestamp, userID, taskID, and eventType.</p>

<h2>Prerequisites</h2>

<ul>
  <li>Python 3.x</li>
  <li>Flask</li>
</ul>

<h2>Installation</h2>

<p>Ensure that you have Python installed on your system. If not, you can download it from the official Python website.</p>

<p>Install Flask using pip. Open your terminal and run the following command:</p>

<pre>
<code>
pip install flask
</code>
</pre>

<h2>Usage</h2>

<p>Run the application by executing the following command in your terminal:</p>

<pre>
<code>
python app.py
</code>
</pre>

<p>Open a web browser and navigate to <code>http://localhost:5000</code>.</p>

<p>Use the form on the web page to upload your CSV file.</p>

<h2>Functionality</h2>

<p>The application performs the following steps:</p>

<ol>
  <li>Reads the uploaded CSV file.</li>
  <li>Splits the data into columns: 'timestamp', 'userID', 'taskID', 'eventType'.</li>
  <li>Cleans the data by stripping any leading or trailing spaces.</li>
  <li>Converts the timestamp to a datetime object and the eventType to a string.</li>
  <li>Sorts the data by timestamp.</li>
  <li>Calculates the total time spent by each user on each task and identifies any discrepancies in the event logs.</li>
</ol>

<p>Discrepancies can occur in the following cases:</p>

<ul>
  <li>A task is started again without being stopped or completed.</li>
  <li>A task is stopped or completed without being started.</li>
  <li>An unknown eventType is found.</li>
  <li>No data is found in one or more columns (UserID, taskID, timestamp, eventType).</li>
  <li>No stopped or completed event is found after a started event.</li>
</ul>

<p>The application generates a report containing the total time spent by each user on each task and any discrepancies found in the event logs. The report is displayed on the web page.</p>

<h2>Note</h2>

<p>This application assumes that the timestamp in the CSV file is in Unix time (seconds since 1970-01-01 00:00:00 UTC).</p>
