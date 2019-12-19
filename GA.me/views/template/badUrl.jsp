<!DOCTYPE html>
<html>
<head>
	<title>GA.me</title>
	<%@ include file = "import.jsp" %>
	<meta http-equiv="refresh" content='5;url=<%= request.getContextPath() %>/views/home.jsp' />
</head>
<body>

	<!--Header Section-->
	<%@ include file = "header.jsp" %>

	<!--Content-->
	<div class="bg-midnight main-content text-center">
		<img src="../../assets/misc/warning.png" width="25%">
		<h1 class="text-light m-4">Bad Access!</h1>
		<h2 class="text-light">You'll be redirected to home page in 5 seconds...</h2>
		<br>
		<div class="d-inline">
			<a href="javascript: history.back()">
				<button type="button" class="btn custom-btn">Back</button>
			</a>
			<a href='<%= request.getContextPath() %>/views/home.jsp'>
				<button type="button" class="btn custom-btn">Home</button>
			</a>
		</div>
	</div>

	<!--Footer Section-->
	<%@ include file = "footer.jsp" %>

</body>
</html>