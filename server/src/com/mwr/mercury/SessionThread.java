// License: Refer to the README in the root directory

package com.mwr.mercury;
import java.lang.reflect.Method;
import java.util.ArrayList;

import android.util.Log;

class SessionThread extends Thread
{
	Session currentSession;
  
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
				try
				{
					// Do some hard work to get the class name
					StringBuilder className = new StringBuilder(
							currentSession.applicationContext.getPackageName() + ".commands.");
					String section = parsedCommands.get(i).section;
					className.append(Character.toUpperCase(section.charAt(0)))
					.append(section.substring(1).toLowerCase());
					
					// Search for the class that represents a section
					Class<?> c = Class.forName(className.toString());
					if (null != c)
					{
						Method[] methods = c.getMethods();
						for (Method method : methods)
						{
							// If method name equals function name, execute the command
							if (method.getName().equalsIgnoreCase(parsedCommands.get(i).function)
									&& null != method)
							{
								found = true;
								method.invoke(null, parsedCommands.get(i).argsArray, currentSession);
								break;
							}
						}
					}
				}
				catch (Exception e)
				{
					currentSession.sendFullTransmission("", "Command not found on Mercury server");
				}
			}
			
			//Default case if command not found
			if (!found)
				currentSession.sendFullTransmission("", "Command not found on Mercury server");
	  }
  
  
}
