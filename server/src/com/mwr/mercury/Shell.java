// License: Refer to the README in the root directory

package com.mwr.mercury;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileDescriptor;
import java.io.FileInputStream;
import java.io.FileOutputStream;

import android.util.Log;

public class Shell
{
	private FileDescriptor termFd;
	public int processId;
	
	public Shell()
	{
		newShell();
	}
	
	//Create a new shell
	public boolean newShell()
	{
		try
		{
			String[] args = {"-"};
			int[] processIdArray = new int[1];
			
			//Create new shell
			termFd = Exec.createSubprocess("/system/bin/sh", args, null, processIdArray);
			processId = processIdArray[0];
			
			//Change cwd to mercury data folder
			write("cd /data/data/com.mwr.mercury");
			//read(); -- this was done as per luander's suggestion
			
			return true;
		}
		catch (Exception e)
		{
			return false;
		}
	}
	
	//Close the file descriptor
	public void closeShell()
	{
		try
		{
			Exec.close(termFd);
		}
		catch (Exception e) {}
		
	}
	
	//Write a command to the shell
	public boolean write(String command)
	{
		try
		{
			BufferedOutputStream termOut = new BufferedOutputStream(new FileOutputStream(termFd));
			termOut.write((command + "\n").getBytes());
			termOut.flush();
			termOut.close();
			
			return true;
		}
		catch (Exception e)
		{
			return false;
		}
	}
	
	//Read from the shell stream
	public String read()
	{
		String returnVal = "";
		BufferedInputStream termIn = new BufferedInputStream(new FileInputStream(termFd));
		
		try
		{
			int newByte = 0;
			
			// Get the Android version of the Device
			int currentapiVersion = android.os.Build.VERSION.SDK_INT;
			if (currentapiVersion >= 14){ // 14 -> The Ice Cream Sandwich API version.
				while (true)
				{
					// Terminal lines in ICS are different of the ones in Gingerbread
					if (returnVal.equals("") || (!returnVal.endsWith(" $ ") && 
							!returnVal.endsWith(" # ") && (newByte != -1)))
					{
						newByte = termIn.read();
					}
					else
					{
						break;
					}
					returnVal += (char)newByte;
				}
			} else{
				while (!returnVal.endsWith("\r\n$ ")
						&& !returnVal.contains("\r\n# ") && (newByte != -1))
				{
					newByte = termIn.read();
					returnVal += (char)newByte;
				}
			}

		}
		catch (Exception e)
		{
			Log.e("mercury", e.getMessage());
		}
		
		return returnVal;
	}
	
}
