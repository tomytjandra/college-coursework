import jess.JessException;
import jess.Rete;

public class Main
{
	public static Rete rete = new Rete();
	
	public static void main(String[] args)
	{
		// TODO Auto-generated method stub
		try
		{
			rete.batch("ticder.clp");
			rete.reset();
			rete.run();
		}
		catch (JessException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
