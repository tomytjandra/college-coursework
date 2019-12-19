<%@page import="java.util.Date, java.text.SimpleDateFormat" %>

<%!
	//Get current date and then change the date format
	Date date = new Date();
	SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy");
	String dateString = sdf.format(date);
%>

<!--Footer Section-->
<footer class="footer bg-dark2">
	<div class="container text-center text-secondary py-3">
		<p class="my-0">Current Date: <%= dateString %> </p>
		<p class="my-0">Copyright &copy;2017 GA</p>
	</div>
</footer>