<!--Header Section-->
<header class="bg-dark2">
	<div class="container">
		<div class="row">
			<div class="col-md-10 offset-md-1">
				<nav class="navbar navbar-dark navbar-expand">
					<!--Navbar Title-->
			 		<a class="navbar-brand font-weight-bold" href="<%= request.getContextPath() %>/views/home.jsp">GA.me</a>

			 		<!--Navbar Menu-->
			 		<div class="collapse navbar-collapse" id="navbarText">
			 			<!--Navbar Left Menu-->
			    		<ul class="navbar-nav mr-auto">
						    <li class="nav-item">
						    	<a class="nav-link" href="<%= request.getContextPath() %>/views/games.jsp">GAmes</a>
						    </li>
						    <li class="nav-item">
						    	<a class="nav-link" href="<%= request.getContextPath() %>/views/community.jsp">Community</a>
						    </li>
			    		</ul>

			    		<% 
			    			//Get the logged in user role
			    			String role = "";
			    			if(session.getAttribute("UserRole") != null){
			    				role = session.getAttribute("UserRole").toString();
			    			}
			    		%>

						<!--Navbar Right Menu-->
			    		<ul class="navbar-nav">

			    		<%
			    			//Guest (Non-Logged in user): Login & Register
			    			if(role.equals("")){
			    		%>	    	

						    <li class="nav-item">
						    	<a class="nav-link" href="<%= request.getContextPath() %>/views/login.jsp">Log In</a>
						    </li>
						    <li class="nav-item">
						    	<a class="nav-link" href="<%= request.getContextPath() %>/views/register.jsp">Register</a>
						    </li>	

				    	<%
			    			}else{
			    			//Logged in user
			    		%>

			    			<!--Dropdown menu-->
			    			<li class="nav-item dropdown">
			    				<!--Greeting to user-->
						        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-disabled="true">
						        	Welcome, <%= session.getAttribute("UserName") %>
						        </a>

						        <!--Dropdown menu item-->
						        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
						        	
						        	<%
						        		//Member: Edit Profile
						        		if(role.equals("member")){
						        	%>
						        	
						        	<a class="dropdown-item" href="<%= request.getContextPath() %>/views/updateProfile.jsp">Edit Profile</a>

						        	<%
						        		}
						        	%>
						        	
						        	<%
						        		//Admin: Manage Game, User, Genre, Developer
						        		if(role.equals("admin")){
						        	%>

						        	<a class="dropdown-item" href="<%= request.getContextPath() %>/views/admin/manageGame.jsp">Manage Game</a>
						        	<a class="dropdown-item" href="<%= request.getContextPath() %>/views/admin/manageUser.jsp">Manage User</a>
						        	<a class="dropdown-item" href="<%= request.getContextPath() %>/views/admin/manageGenre.jsp">Manage Genre</a>
						        	<a class="dropdown-item" href="<%= request.getContextPath() %>/views/admin/manageDeveloper.jsp">Manage Developer</a>

						        	<%
						        		}
						        	%>

						        	<div class="dropdown-divider" style="border-color:black;"></div>

						        	<!--Member & Admin: Logout-->
						       		<a class="dropdown-item" href="<%= request.getContextPath() %>/controllers/logoutController.jsp">Logout</a>
								</div>
							</li>

			    		<%
			    			}
			    		%>

			    		</ul>

			  		</div>
				</nav>
			</div>
		</div>
	</div>
</header>