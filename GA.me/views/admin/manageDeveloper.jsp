<%
	//Only admin can access
	if(!session.getAttribute("UserRole").equals("admin")){
		response.sendRedirect(request.getContextPath()+"/views/template/badUrl.jsp");
	}
%>

<%@ include file = "../../controllers/connect.jsp" %>

<!--Pagination-->
<%
	//Get search key parameter (input by user) and search in the database
	String searchKey = "";
	String condition = "";
	if(request.getParameter("search") != null){
		searchKey = request.getParameter("search");
		condition = " WHERE DeveloperName LIKE '%" + searchKey + "%'";
	}

	//Get total data
	String query = "SELECT COUNT(*) FROM developer" + condition;
	ResultSet rs = st.executeQuery(query);
	int totalData = 0;
	if(rs.next()){
		totalData = rs.getInt(1);
	}

	//Calculate total page based on total data and how many row per page
	int developerPerPage = 6;
	int totalPage = (int)Math.ceil(totalData / (double)developerPerPage);

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
	int skipRow = (currentPage - 1)*developerPerPage;
	query = "SELECT * FROM developer" + condition + " LIMIT " + skipRow + ", " + developerPerPage;
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
	
	<!--Manage Developer Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Manage Developer Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Manage GAmes</h4>
					<p class="text-secondary">Popular game in GAme</p>
				</div>
			</div>

			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10 box-content">
					<div class="row">
						<!--Insert New Developer Button-->
						<div class="col-md-6">
							<form action="insertDeveloper.jsp" method="POST" class="form-inline">
								<div class="form-group">
									<input type="submit" class="btn custom-btn" value="Insert New Developer">
								</div>
							</form>
						</div>
						<!--Search developer by its name-->
						<div class="col-md-6">
							<form action="#" method="GET" class="form-inline">
								<div class="form-group">
									<label class="text-light">Search Developers:</label>
									<input type="text" name="search" class="form-control custom-input my-0 mx-2">
								</div>
								<div class="form-group">
									<input type="submit" class="btn custom-btn" value="Search">
								</div>
							</form>
						</div>
					</div>
				</div>
			</div>

			<!--Loop Developer-->
			<%
				while(rs.next())
				{
			%>
			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10 custom-list-item">
					<div class="row">
						<!--Developer Name-->
						<div class="col-md-10 p-4">
							<p class="text-light m-0">
								<%= rs.getString("DeveloperName") %>									
							</p>
						</div>

						<div class="col-md-2">
							<!--Update Developer Button-->
							<form action="updateDeveloper.jsp" method="POST">
								<div class="form-group">
									<input type="hidden" name="developerId" value='<%= rs.getString("DeveloperId") %>'>
									<input type="submit" class="btn btn-success" value="Update" style="width:100%">
								</div>
							</form>

							<!--Delete Developer Button-->
							<button type="button" class="btn btn-danger deleteModal" data-toggle="modal" data-target="#deleteModal" data-developer-id = "<%= rs.getString("DeveloperId") %>" data-developer-name = "<%= rs.getString("DeveloperName") %>" style="width:100%">
								Delete
							</button>

							<!--Modal (Pop Up) for Delete-->
							<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalCenterTitle" aria-hidden="true">
								<div class="modal-dialog modal-dialog-centered" role="document">
							    	<div class="modal-content">
							      		<div class="modal-header">
							        		<h5 class="modal-title" id="deleteModalLongTitle">Delete Developer</h5>
							        		<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							          			<span aria-hidden="true">&times;</span>
							        		</button>
							      		</div>
									    <div class="modal-body">
									    	<!--Must assign developerName outside the while loop (in JS)-->
									    	Are you sure you want to delete <p id="developerName" class="d-inline"></p>?
									    </div>
										<div class="modal-footer">
									    	<button type="button" class="btn btn-secondary" data-dismiss="modal">No</button>
									    	<form action="../../controllers/admin/doDeleteDeveloper.jsp" method="POST">
									    		<!--Must assign developerId value outside the while loop (in JS)-->
									    		<input type="hidden" id="developerId" name="developerId" value="">
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
							href='manageDeveloper.jsp?page=
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
							href='manageDeveloper.jsp?page=
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
							href='manageDeveloper.jsp?page=
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
	            var developerId = $(this).data('developer-id');
	            document.getElementById('developerId').value = developerId;

	            var developerName = $(this).data('developer-name');
	            document.getElementById('developerName').innerHTML = developerName;
	        })
	    });
	</script>

</body>
</html>