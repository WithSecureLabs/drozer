// License: Refer to the README in the root directory

package com.mwr.mercury;
import java.util.ArrayList;

import android.util.Log;

class SessionThread extends Thread
{
	Session currentSession;
  
	//Server version info
	String version_info = "Mercury v0.1";
  
	//Assign session variables
	SessionThread(Session session)
	{
		currentSession = session;
	}
	
	@Override
	protected void finalize() throws Throwable
	{
		// TODO Auto-generated method stub
		super.finalize();
		Log.e("mercury", "Closing thread");
	}
  
	//This thread receives commands from the client and handles command
	public void run()
	{
		while (currentSession.connected)
		{
			//Pass off command to be handled
			handleCommand(currentSession.receive());
		}
		Log.e("mercury", "Exiting thread");
	}
  
  
	//Redirect commands to be handled by different functions
	public void handleCommand(String xmlInput)
	{
		//Create an array of commands from xml request received
		ArrayList<RequestWrapper> parsedCommands = new XML(xmlInput).getCommands();
		
		//Command has been found on server
		boolean found = false;
	
		//Iterate through received commands
		for (int i = 0; i < parsedCommands.size(); i++)
		{
			//Look for server command and execute
			for (CommandWrapper command : Commands.commandList)
			{
				if (parsedCommands.get(i).section.toUpperCase().equals(command.section.toUpperCase()) && parsedCommands.get(i).function.toUpperCase().equals(command.function.toUpperCase()))
				{
					found = true;
					command.executor.execute(parsedCommands.get(i).argsArray, currentSession);
					break;
				}
	        }
		}
		
		//Default case if command not found
		if (!found)
			currentSession.sendFullTransmission("", "Command not found on Mercury server");
  }
  
  
}
