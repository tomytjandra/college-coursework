import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.GridLayout;
import java.awt.Image;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.util.Vector;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;

import jess.JessException;
import jess.QueryResult;
import jess.ValueVector;


public class Template extends JFrame
{	
	JPanel content_panel = new JPanel(new FlowLayout(FlowLayout.CENTER, 30, 30));
	
	JButton btnClose = new JButton("Close");
	
	String userName = "";
	String userAge = "";
	String userGender = "";
	String userHeight = "";
	String userHobby = "";
	String userInterest = "";
	String userPreferredIncome = "";
	
	Vector<String> header = new Vector<String>();
	Vector<Vector<String>> data = new Vector<Vector<String>>();
	Vector<String> row;
	
	DefaultTableModel defaultTableModel;
	JTable table;
	JScrollPane scrollPane;
	
	final Template frame = this;
	
	public void initComponents()
	{
		getContentPane().setLayout(new BorderLayout());
		
		JLabel lblTitle = new JLabel("No Match Found!", JLabel.CENTER);
		lblTitle.setFont(new Font(Font.MONOSPACED, Font.BOLD, 21));
		getContentPane().add(lblTitle, BorderLayout.NORTH);
		
		JPanel left_panel = new JPanel(new BorderLayout());
		JLabel lblHeader = new JLabel("Your Profile");
		lblHeader.setFont(new Font(Font.MONOSPACED, Font.BOLD, 15));
		left_panel.add(lblHeader, BorderLayout.NORTH);
		
		//Panel that contain all user's info
		JPanel grid_panel = new JPanel(new GridLayout(7, 2));
		
		JLabel lblName = new JLabel("Name : ");
		JLabel lblAge = new JLabel("Age : ");
		JLabel lblGender = new JLabel("Gender : ");
		JLabel lblHeight = new JLabel("Height  : ");
		JLabel lblHobby = new JLabel("Hobby  : ");
		JLabel lblInterest = new JLabel("Interest : ");
		JLabel lblIncome = new JLabel("Prefered Income : ");

		//Labels that contain user's info
		JLabel lblNameInfo = new JLabel();
		JLabel lblAgeInfo = new JLabel();
		JLabel lblGenderInfo = new JLabel();
		JLabel lblHeightInfo = new JLabel();
		JLabel lblHobbyInfo = new JLabel();
		JLabel lblInterestInfo = new JLabel();
		JLabel lblIncomeInfo = new JLabel();
		
		try
		{
			QueryResult resultMatchUser = Main.rete.runQueryStar("matchUserQuery", new ValueVector());
			
			if(resultMatchUser.next())
			{
				userName = resultMatchUser.getString("name");
				userAge = resultMatchUser.getString("age");
				userGender = resultMatchUser.getString("gender");
				userHeight = resultMatchUser.getString("height");
				userHobby = resultMatchUser.getString("hobby");
				userInterest = resultMatchUser.getString("interest");
				userPreferredIncome = resultMatchUser.getString("preferredIncome");
				
				lblNameInfo.setText(userName);
				lblAgeInfo.setText(userAge);
				lblGenderInfo.setText(userGender);
				lblHeightInfo.setText(userHeight);
				lblHobbyInfo.setText(userHobby);
				lblInterestInfo.setText(userInterest);
				lblIncomeInfo.setText(userPreferredIncome);
				
				if(userInterest.equals("Female"))
				{
					lblIncome.hide();
					lblIncomeInfo.hide();
				}
			}
			
			resultMatchUser.close();
		}
		catch (JessException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		//Object that can be used as panel that contain image or table
		Object panel_add = null;
		
		//No match found
		panel_add = imageNotAvailable();
		
		/*Fill the code here to fetch all suitable match for user*/
		
		header.add("No.");
		header.add("name");
		header.add("hobby");
		header.add("height");
		if(userInterest.equals("Male"))header.add("income");
		header.add("match-rate");
		
		defaultTableModel = new DefaultTableModel(data, header);
		table = new JTable(defaultTableModel);
		scrollPane = new JScrollPane(table);
		
		int index = 0;
		
		if(userInterest.equals("Male"))
		{
			try
			{
				QueryResult resultMatchMale = Main.rete.runQueryStar("matchMaleQuery", new ValueVector());
				
				while(resultMatchMale.next())
				{
					index++;
					
					String name = resultMatchMale.getString("name");
					String hobby = resultMatchMale.getString("hobby");
					String height = resultMatchMale.getString("height");
					String income = resultMatchMale.getString("income");
					String matchRate = resultMatchMale.getString("match-rate");
					
					row = new Vector<String>();
					
					row.add(Integer.toString(index));
					row.add(name);
					row.add(hobby);
					row.add(height);
					row.add(income+" $USD");
					row.add(matchRate+"%");
					
					//System.out.println(resultMatchMale.getString("age"));
					
					data.add(row);
				}
				
				resultMatchMale.close();
				
				
			}
			catch (JessException e)
			{
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		else if(userInterest.equals("Female"))
		{
			try
			{
				QueryResult resultMatchFemale = Main.rete.runQueryStar("matchFemaleQuery", new ValueVector());
				
				while(resultMatchFemale.next())
				{
					index++;
					
					String name = resultMatchFemale.getString("name");
					String age = resultMatchFemale.getString("age");
					String hobby = resultMatchFemale.getString("hobby");
					String height = resultMatchFemale.getString("height");
					String matchRate = resultMatchFemale.getString("match-rate");
					
					row = new Vector<String>();
					
					row.add(Integer.toString(index));
					row.add(name);
					row.add(hobby);
					row.add(height);
					row.add(matchRate+"%");
					
					//System.out.println(resultMatchFemale.getString("age"));
					
					data.add(row);
				}
				
				resultMatchFemale.close();
				
				
			}
			catch (JessException e)
			{
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		if(data.size() != 0 )
		{
			panel_add = scrollPane;
			lblTitle.setText("Matches Found!");
		}
		
		grid_panel.add(lblName);
		grid_panel.add(lblNameInfo);
		
		grid_panel.add(lblAge);
		grid_panel.add(lblAgeInfo);
		
		grid_panel.add(lblGender);
		grid_panel.add(lblGenderInfo);
		
		grid_panel.add(lblHeight);
		grid_panel.add(lblHeightInfo);
		
		grid_panel.add(lblHobby);
		grid_panel.add(lblHobbyInfo);
		
		grid_panel.add(lblInterest);
		grid_panel.add(lblInterestInfo);
		
		grid_panel.add(lblIncome);
		grid_panel.add(lblIncomeInfo);
		
		left_panel.add(grid_panel, BorderLayout.CENTER);
		
		content_panel.add(left_panel);
		content_panel.add((Component) panel_add);
		content_panel.setPreferredSize(new Dimension (800, 450));
		
		getContentPane().add(content_panel, BorderLayout.CENTER);
		getContentPane().add(btnClose, BorderLayout.PAGE_END);
		
		btnClose.addActionListener(new ActionListener()
		{
			
			@Override
			public void actionPerformed(ActionEvent arg0)
			{
				frame.dispose();
			}
		});
	}
	
	private Image getScaledImage(Image srcImage, int width, int height)
	{
		BufferedImage resizedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
		Graphics2D g2d = resizedImage.createGraphics();
		
		g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BICUBIC);
		g2d.drawImage(srcImage, 0, 0, width, height, null);
		g2d.dispose();
		
		return resizedImage;
	}
	
	public JLabel imageNotAvailable()
	{
		JLabel lbl_img = new JLabel();
		lbl_img.setPreferredSize(new Dimension(320,180));
		Image bufferedImage;
		try
		{
			bufferedImage = ImageIO.read(getClass().getResource("not_available.jpg"));
			ImageIcon icon = new ImageIcon(getScaledImage(bufferedImage, 320, 180));
			lbl_img.setIcon(icon);
		}
		catch (IOException e)
		{
			return null;
		}
		return lbl_img;
	}
	
	public Template()
	{
		setTitle("The Result of Consultation");
		setSize(850, 450);
		setLocationRelativeTo(null);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		initComponents();
		setResizable(false);
		setVisible(true);
	}
}