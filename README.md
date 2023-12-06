# ScreenSeat

<h1>Project Overview</h1>
<p>SelectSeat is a comprehensive ticket booking system for movies, designed to facilitate easy and efficient show and theatre management. This system is crafted with a robust stack of technologies and offers a seamless user experience for both general users and administrators.</p>

<h2>Technology Stack</h2>
<ul>
    <li>Frontend: VueJS for UI, optionally using VueJS Advanced with CLI. Jinja2 templates for dynamic content rendering.</li>
    <li>Styling: Bootstrap for CSS, with no other CSS frameworks allowed.</li>
    <li>Backend: Flask for API development.</li>
    <li>Database: SQLite as the primary database system.</li>
    <li>Caching and Batch Jobs: Redis for caching and batch jobs management with Redis and Celery.</li>
    <li>Compatibility: Designed for Linux-based systems, compatible with Windows OS via WSL.</li>
</ul>

<h2>Functionality</h2>
<ul>
    <li>User Signup and Login</li>
    <li>Mandatory Admin Login with RBAC</li>
    <li>Theatre and Show Management</li>
    <li>Booking Show Tickets</li>
    <li>Search for Shows/Theatres</li>
    <li>Backend Jobs (Export, Reporting, Alert Jobs)</li>
    <li>Backend Performance Optimization</li>
</ul>

<h2>System Design</h2>
<h3>User's Side</h3>
<p>Enables users to book tickets for shows. Interface built with HTML, CSS (Bootstrap), and VueJS. Communication with the backend through REST APIs.</p>
<h3>Admin Side</h3>
<p>Allows creation and management of shows. Admin functionalities are protected by RBAC.</p>

<h3>Architecture</h3>
<ul>
    <li>Frontend: HTML and CSS with Bootstrap styling.</li>
    <li>Backend: Flask script hosted locally, with SQLAlchemy for database interaction.</li>
    <li>Communication between frontend and backend via REST APIs.</li>
    <li>Dynamic content rendering using Jinja2 in Flask.</li>
</ul>

<h2>Security</h2>
<p>Utilizes Flask-Login for secure user and admin authentication. Restricts access to certain pages for non-logged-in users.</p>

<h2>Database Models</h2>
<p>The application uses Flask-SQLAlchemy for database management. Below are the models representing the database structure:</p>

<h3>User Model</h3>
<table>
    <tr><th>Field</th><th>Type</th></tr>
    <tr><td>id</td><td>Integer</td></tr>
    <tr><td>username</td><td>String(50)</td></tr>
    <tr><td>password</td><td>String(100)</td></tr>
    <tr><td>isAdmin</td><td>Integer</td></tr>
</table>

<h3>Venue Model</h3>
<table>
    <tr><th>Field</th><th>Type</th></tr>
    <tr><td>id</td><td>Integer</td></tr>
    <tr><td>venue_name</td><td>String(50)</td></tr>
    <tr><td>venue_description</td><td>String(50)</td></tr>
    <tr><td>venue_location</td><td>String(50)</td></tr>
    <tr><td>venue_capacity</td><td>String(50)</td></tr>
</table>

<h3>Show Model</h3>
<table>
    <tr><th>Field</th><th>Type</th></tr>
    <tr><td>id</td><td>Integer</td></tr>
    <tr><td>show_name</td><td>String(50)</td></tr>
    <tr><td>show_rating</td><td>String(50)</td></tr>
    <tr><td>show_rating_count</td><td>Integer</td></tr>
    <tr><td>show_date</td><td>String(50)</td></tr>
    <tr><td>show_time</td><td>String(50)</td></tr>
    <tr><td>show_price</td><td>String(50)</td></tr>
    <tr><td>show_tags</td><td>String(50)</td></tr>
    <tr><td>show_capacity</td><td>Integer</td></tr>
    <tr><td>show_available_tickets</td><td>Integer</td></tr>
    <tr><td>venue_id</td><td>Integer (ForeignKey)</td></tr>
</table>

<h3>Booking Model</h3>
<table>
    <tr><th>Field</th><th>Type</th></tr>
    <tr><td>id</td><td>Integer</td></tr>
    <tr><td>tickets</td><td>Integer</td></tr>
    <tr><td>total_price</td><td>Integer</td></tr>
    <tr><td>show_id</td><td>Integer (ForeignKey)</td></tr>
    <tr><td>user_id</td><td>Integer (ForeignKey)</td></tr>
    <tr><td>show_rating</td><td>Integer</td></tr>
</table>
