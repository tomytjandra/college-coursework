<%
	//Only admin can access
	if(!session.getAttribute("UserRole").equals("admin")){
		response.sendRedirect(request.getContextPath()+"/views/template/badUrl.jsp");
	}
%>

<%@ include file = "../../controllers/connect.jsp" %>

<!--Pagination, only role member-->
<%
	//Get search key parameter (input by user) and search in the database
	String searchKey = "";
	String condition = "";
	if(request.getParameter("search") != null){
		searchKey = request.getParameter("search");
		condition = " AND UserName LIKE '%" + searchKey + "%'";
	}

	//Get total data
	String query = "SELECT COUNT(*) FROM user WHERE UserRole = 'member'" + condition;
	ResultSet rs = st.executeQuery(query);
	int totalData = 0;
	if(rs.next()){
		totalData = rs.getInt(1);
	}

	//Calculate total page based on total data and how many row per page
	int userPerPage = 6;
	int totalPage = (int)Math.ceil(totalData / (double)userPerPage);

	//Get current page
	int currentPage = 1;
	if(request.getParameter("page") != null){
		try{
			currentPage = Integer.parseInt(request.getParameter("page"));
		}catch(Exception ex){
			currentPage = 1;
		}
	}

	//Select row based on search key and current page
	int skipRow = (currentPage - 1)*userPerPage;
	query = "SELECT * FROM user WHERE UserRole = 'member'" + condition + " LIMIT " + skipRow + ", " + userPerPage;
	rs = st.executeQuery(query);
%>

<!DOCTYPE html>
<html>
<head>
	<title>GA.me</title>
	<%@ include file = "../template/import.jsp" %>
</head>
<body>

	<!--Header Section-->
	<%@ include file = "../template/header.jsp" %>
	
	<!--Manage User Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Manage User Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Users</h4>
				</div>
			</div>

			<div class="row">
				<div class="col-md-1"></div>
				<!--Search user (role: member) by its name-->
				<div class="col-md-10 box-content">
					<form action="manageUser.jsp" method="GET" class="form-inline">
						<div class="form-group">
							<label class="text-light">Search users:</label>
							<input type="text" name="search" class="form-control custom-input my-0 mx-2">
						</div>
						<div class="form-group">
							<input type="submit" class="btn custom-btn" value="Search">
						</div>
					</form>
				</div>
			</div>

			<!--Loop User-->
			<%
				while(rs.next())
				{
			%>
			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10 custom-list-item">
					<div class="row">
						<!--User Picture, use default.png if not set-->
						<div class="col-md-2" style="text-align: center;">
							<img src="../../assets/userpictures/
							<%= rs.getString("UserPicture")==null? "default.png" : rs.getString("UserPicture")%>" width="125px" height="125px">
						</div>

						<!--User Information-->
						<div class="col-md-6">
							<p class="text-light m-0"><%= rs.getString("UserName")%></p>
							<p class="text-secondary"><%= rs.getString("UserEmail")%></p>
						</div>
						<div class="col-md-2">
							<p class="text-light"><%= rs.getString("UserRole")%></p>
						</div>

						<div class="col-md-2">
							<!--Delete Game Button-->
							<button type="button" class="btn btn-danger deleteModal" data-toggle="modal" data-target="#deleteModal" data-user-id = "<%= rs.getString("UserId") %>" data-user-name = "<%= rs.getString("UserName") %>" style="width:100%">
								Delete
							</button>

							<!--Modal (Pop Up) for Delete-->
							<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalCenterTitle" aria-hidden="true">
								<div class="modal-dialog modal-dialog-centered" role="document">
							    	<div class="modal-content">
							      		<div class="modal-header">
							        		<h5 class="modal-title" id="deleteModalLongTitle">Delete User</h5>
							        		<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							          			<span aria-hidden="true">&times;</span>
							        		</button>
							      		</div>
									    <div class="modal-body">
									    	<!--Must assign userName outside the while loop (in JS)-->
									    	Are you sure you want to delete <p id="userName" class="d-inline"></p>?
									    </div>
										<div class="modal-footer">
									    	<button type="button" class="btn btn-secondary" data-dismiss="modal">No</button>
									    	<form action="../../controllers/admin/doDeleteUser.jsp" method="POST">
									    		<!--Must assign userId value outside the while loop (in JS)-->
									    		<input type="hidden" id="userId" name="userId" value="">
									    		<input type="submit" class="btn btn-danger" value="Yes">
									    	</form>
									 	</div>
							    	</div>
							  	</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<%
				}
			%>

			<!--Pagination-->
			<div class="row">
				<div class="col-md-12">
					<ul class="pagination justify-content-center">
						
						<!--Prev button, disabled when currentPage == 1-->
						<li class="page-item
							<% if(currentPage==1){out.println("disabled");} %> ">
							<a class="page-link" 
							href='manageUser.jsp?page=
							<%= currentPage-1 %>
							<%= condition.equals("")? "" : "&search=" + request.getParameter("search")%>'>
								Prev
							</a>
						</li>
						
						<!--Loop pagination button, from 1 until totalPage-->
						<%
							for(int i=1; i<=totalPage; i++)
							{
						%>
						<li class="page-item 
							<% if(i==currentPage){out.println("active");} %> ">
							<a class="page-link" 
							href='manageUser.jsp?page=
							<%= i %>
							<%= condition.equals("")? "" : "&search=" + request.getParameter("search")%>'>
								<%= i %>
							</a>
						</li>
						<%
							}
						%>

						<!--Next button, disabled when currentPage == totalPage-->
						<li class="page-item
							<% if(currentPage==totalPage){out.println("disabled");} %> ">
							<a class="page-link" 
							href='manageUser.jsp?page=
							<%= currentPage+1 %>
							<%= condition.equals("")? "" : "&search=" + request.getParameter("search")%>'>
								Next
							</a>
						</li>

					</ul>
				</div>
			</div>
		</div>
	</div>

	<!--Footer Section-->
	<%@ include file = "../template/footer.jsp" %>

	<!-- JS for Delete Modal -->
	<script type="text/javascript">
	    $(function () {
	        $(".deleteModal").click(function () {
	            var userId = $(this).data('user-id');
	            document.getElementById('userId').value = userId;

	            var userName = $(this).data('user-name');
	            document.getElementById('userName').innerHTML = userName;
	        })
	    });
	</script>

</body>
</html>