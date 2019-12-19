<%
	//Only admin can access
	if(!session.getAttribute("UserRole").equals("admin")){
		response.sendRedirect(request.getContextPath()+"/views/template/badUrl.jsp");
	}
%>

<%@ include file = "../../controllers/connect.jsp" %>

<!DOCTYPE html>
<html>
<head>
	<title>GA.me</title>
	<%@ include file = "../template/import.jsp" %>
</head>
<body>

	<!--Header Section-->
	<%@ include file = "../template/header.jsp" %>
	
	<!--Insert Developer Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Insert Developer Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Insert</h4>
				</div>
			</div>

			<div class="row">
				<div class="col-md-1"></div>
				<!--Insert Developer Form-->
				<div class="col-md-6 box-content">
					<h6 class="text-light font-weight-bold">Create</h6>
					<p class="text-secondary">A new Developer.</p>

					<form action="../../controllers/admin/doInsertDeveloper.jsp" method="POST">
						<!--Name text field-->
						<div class="form-group">
							<label class="text-light">Name</label>
							<input type="text" name="txtName" class="form-control custom-input" placeholder="Name">
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errName")!=null){
										out.print(request.getParameter("errName"));
									}
								%>
							</span>
						</div>

						<!--Insert Developer button-->
						<div class="form-group">
							<input type="submit" class="btn btn-primary" value="Insert Developer">
						</div>
					</form>
				</div>

				<!--Content-->
				<div class="col-md-4 box-content text-light">
					<div class="m-1">
						<h6 class="text-light font-weight-bold">Why join GAme?</h6>
						<ul class="text-secondary">
							<li>Discover lots of games</li>
							<li>Join the GAme Community</li>
							<li>Find a new friends</li>
							<li>Debate with a new friends</li>
							<li>Schedule a game, tournament, or LAN party</li>
							<li>Never miss game updates, and more!</li>
						</ul>
					</div>

					<div class="m-1">
						<a href='<%= request.getContextPath() %>/views/games.jsp' class="text-primary font-weight-bold">Instant Access to Games</a>
						<p class="text-secondary">We have thousands of games from Action to Indie and everything in-between. Join us and win the game.</p>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!--Footer Section-->
	<%@ include file = "../template/footer.jsp" %>

</body>
</html>