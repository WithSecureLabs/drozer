import java.io.InputStream;
import java.io.OutputStream;
import java.lang.Exception;
import java.io.FileDescriptor;

import android.net.LocalServerSocket;
import android.net.LocalSocket;

public class JdwpBroker
{
	private LocalServerSocket jdwp_control;
	private LocalSocket jdwp_socket;
	private InputStream jdwp_socket_input;
	private OutputStream jdwp_socket_output;

	public JdwpBroker()
	{

	}

	//Returns error, if any
	public String openJdwpControl()
	{
		try
		{
			jdwp_control = new LocalServerSocket("jdwp-control");
			return "";
		}
		catch (Exception e)
		{
			return e.getMessage();
		}
	}

	public void closeJdwpControl()
	{
		try
		{
			jdwp_control.close();
		}
		catch (Exception e)
		{

		}
	}

	//Returns connected UID: -1 for error
	public int acceptConnection()
	{
		try
		{
			jdwp_socket = jdwp_control.accept();
			jdwp_socket_input = jdwp_socket.getInputStream();
			jdwp_socket_output = jdwp_socket.getOutputStream();
			return jdwp_socket.getPeerCredentials().getUid();	
		}
		catch (Exception e)
		{
			return -1;
		}
	}

	public void closeConnection()
	{
		try
		{
			jdwp_socket.close();
		}
		catch (Exception e)
		{

		}
	}

	//Read the PID of the connected app from the socket
	public int readPid()
	{
		try
		{
			byte[] pid = new byte[4];
			int len = jdwp_socket_input.read(pid);

			String returnStr = "";
			for (int i = 0; i < len; i++)
				returnStr += (char) pid[i];

			return Integer.parseInt(returnStr, 16);
		}
		catch (Exception e)
		{
			return -1;
		}
	}
}
