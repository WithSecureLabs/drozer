// License: Refer to the README in the root directory

package com.mwr.mercury;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

import android.content.Context;
import android.util.Base64;
import android.util.Log;

public class Session
{
	private BufferedBracketReader input;
	private PrintWriter output;
	private Socket clientSocket;  
	public boolean connected;
	public Context applicationContext;

	//Assign session information
	Session(Socket client, Context ctx)
	{
		clientSocket = client;
		applicationContext = ctx;
		connected = true;
		
		try
		{
			//input = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()), 8192);
			input = new BufferedBracketReader(new InputStreamReader(clientSocket.getInputStream()));
			output = new PrintWriter(clientSocket.getOutputStream(), true);
		}
		catch (Exception e) {}
		
		Log.e("mercury", "New session from " + clientSocket.getInetAddress().toString());
	}
	
	//Read from session - return contents
	public String receive()
	{
		try
		{
			//Wait until ready
			//while (!input.ready());
			
			//Read from socket
			//String content = input.readLine();
			String content = readTransmission(input);
					
			//Maintain whether connection is still connected or not
			if (content == null)
				connected = false;
			else
				connected = true;
			
			return content;
		}
		catch (IOException e)
		{
			connected = false;
			return null;
		}
	}
	
	private String readTransmission(BufferedBracketReader in) throws IOException
	{
		//String out = "";
		//StringBuilder sb = new StringBuilder(512);
		//int cur = in.read();
		//while(cur == '\n' || cur  == '\r' || cur == ' ') cur = in.read();
		String out = "";
		in.skipWs();
		while(true) {
			//Log.d("RECV", "before");
			String r = in.readChunk();
			//Log.d("RECV", "after");
			if(r!=null) {
				//Log.d("RECV", r);
				out += r;
				if(out.endsWith("</transmission>")) {
					return out;
				}
			}
			/*
			sb.append((char)cur);
			 
			if (cur == (char)'>') {
				String out = sb.toString();
				if(out.endsWith("</transmission>"))
					return out;
			}
			cur = in.read();
			*/
		}
	}

	//Write to session - return success
	public boolean send(String data, boolean base64)
	{
		try
		{
			//Write to socket base64 encoded with a newline on end
			if (base64)
				output.print(new String(Base64.encode(data.getBytes(), Base64.DEFAULT)) + "\n");
			else
			//Or not
				output.print(data);
			
			output.flush();
			
			return true;
		}
		catch (Exception e)
		{
			return false;
		}
	}
	
	//Send start of transmission tag
	public void startTransmission()
	{
		send("<?xml version=\"1.0\" ?><transmission>", false);	  
	}
	
	//Send start of response tag
	public void startResponse()
	{
		send("<response>", false);
	}
	
	//Send end of response tag
	public void endResponse()
	{
		send("</response>", false);
	}
	
	//Send error tag with contents
	public void error(String error)
	{
		send("<error>", false);
		send(error, true);
		send("</error>", false);
	}
	
	//Send error tag with no contents
	public void noError()
	{
		send("<error />", false);
	}
	
	//Send start of data tag
	public void startData()
	{
		send("<data>", false);
	}
	
	//Send end of data tag
	public void endData()
	{
		send("</data>", false);
	}
	
	//Send end of transmission tag and close socket
	public void endTransmission()
	{
		//Send close of transmission
		send("</transmission>", false);
		
		//Set connected to false so that server does not keep listening on this conn
		// connected = false;
		
		//Kill socket
		//try
		//{
		//	clientSocket.close();
		//}
		//catch (IOException e) {}
	}
	
	//Send a full transmission without worrying about structure
	//Should only be used for small responses < 50KB
	public void sendFullTransmission(String response, String error)
	{
		/*
		
		Sends the following structure:
		
		<transmission>
			<response>
				<data>response</data>
				<error>error</error>
			</response>
		</transmission>
		
		*/
		
		startTransmission();
		startResponse();
		startData();
		send(response, true);
		endData();
		
		if (error == null)
			error("Null error given");
		else
			if (error.length() > 0)
				error(error);
			else
				noError();
		
		endResponse();
		endTransmission();
	}
  
  
}
