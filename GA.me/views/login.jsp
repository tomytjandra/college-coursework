<%
	//Only guest can access, logged in user cannot register again
	if(session.getAttribute("UserRole") != null){
		response.sendRedirect(request.getContextPath()+"/views/template/badUrl.jsp");
	}

	//Get email and password cookies from previous log in (when "Remember Me" is checked)
	Cookie[] cookies = request.getCookies();
	String email = "";
	String password = "";

	for(int i=0; i<cookies.length; i++){
		if(cookies[i].getName().equals("UserEmail")){
			email = cookies[i].getValue();
		}else if(cookies[i].getName().equals("UserPassword")){
			password = cookies[i].getValue();
		}
	}
%>

<!DOCTYPE html>
<html>
<head>
	<title>GA.me</title>
	<%@ include file = "template/import.jsp" %>
</head>
<body>

	<!--Header Section-->
	<%@ include file = "template/header.jsp" %>
	
	<!--Login Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Login Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Sign In</h4>
				</div>
			</div>

			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-5 box-content">
					<h6 class="text-light font-weight-bold">Sign In</h6>
					<p class="text-secondary">To an existing GAme account</p>

					<!--Login Form-->
					<form action="../controllers/loginController.jsp" method="POST">
						<!--Account name/Email text field-->
						<div class="form-group">
							<label class="text-light">Account name</label>
							<input type="text" name="txtEmail" class="form-control custom-input" placeholder="Email" value="<%=email%>">
						</div>

						<!--Password text field-->
						<div class="form-group">
							<label class="text-light">Password</label>
							<input type="password" name="txtPassword" class="form-control custom-input" placeholder="Password" value="<%=password%>">
						</div>

						<!--Remember Me checkbox-->
						<div class="form-group">
							<input type="checkbox" name="cbRemember">
							<label class="text-light">Remember Me</label>
						</div>

						<!--Error Message-->
						<div class="form-group">
							<span class="text-danger" id="errLogin">
								<%
									//Display message when there is an error
									if(request.getParameter("errMsg")!=null){
										out.print(request.getParameter("errMsg"));
									}else{
										out.print("&nbsp;");
									}
								%>
							</span>
						</div>

						<!--Login button-->
						<div class="form-group">
							<input type="submit" class="btn custom-btn" value="Sign In">
						</div>
					</form>
				</div>

				<!--Content, Redirect to Register-->
				<div class="col-md-5 box-content">
					<h6 class="text-light font-weight-bold">Create</h6>
					<p class="text-secondary">A new free account</p>
					<p class="text-secondary">It's free to join and easy to use. Continue on to create your Game account and get Game, the leading digital solution for PC, Mac, and Linux games and Software.</p>
					<form action="register.jsp">
						<div class="form-group">
							<input type="submit" class="btn custom-btn" value="Register">
						</div>
					</form>
				</div>
			</div>
		</div>
	</div>

	<!--Footer Section-->
	<%@ include file = "template/footer.jsp" %>

</body>
</html>