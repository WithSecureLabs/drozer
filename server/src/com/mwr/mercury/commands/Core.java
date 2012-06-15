// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import com.mwr.mercury.*;

import android.util.Base64;

public class Core
{
	//core.ping() - returns "pong"
	public static void ping(List<ArgumentWrapper> argsArray, Session currentSession){
		currentSession.sendFullTransmission("pong", "");
	}
	
	//core.version() - returns Mercury version
	public static void version(List<ArgumentWrapper> argsArray, Session currentSession){
		String version = "";
		try
		{
			version = currentSession.applicationContext.getPackageManager().getPackageInfo(currentSession.applicationContext.getPackageName(), 0).versionName;
		}
		catch (Exception e) {}
		currentSession.sendFullTransmission(version, "");
	}
	
	public static void fileSize(List<ArgumentWrapper> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		
		try
		{
			File file = new File(path);
			
			//Send the size of the file
			if (file.exists())
				currentSession.sendFullTransmission(String.valueOf(file.length()), "");
			else
				currentSession.sendFullTransmission("", "File does not exist");
		}
		catch (Exception e)
		{
			currentSession.sendFullTransmission("", e.getMessage());
		}
	}
	
	public static void fileMD5(List<ArgumentWrapper> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		
		try
		{
			//Send the number of bytes in the file
			currentSession.sendFullTransmission(Common.md5SumFile(path), "");
		}
		catch (Exception e)
		{
			currentSession.sendFullTransmission("", e.getMessage());
		}
	}
	
	public static void download(List<ArgumentWrapper> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		Integer offset = Integer.parseInt(Common.getParamString(argsArray, "offset"));
		
		//Start sending structure
		currentSession.startTransmission();
		currentSession.startResponse();
		currentSession.startData();
		
		File file = new File(path);
		InputStream in = null;
		
		int buffSize = 50 * 1024; //50KB
		
		try
		{
			in = new BufferedInputStream(new FileInputStream(file));
			
			byte[] buffer = new byte[buffSize];
			
			for (int i = 0; i < offset; i++)
				in.read();
			
			int bytesRead = in.read(buffer, 0, buffSize);
			
			currentSession.send(new String(Base64.encode(buffer, 0, bytesRead, Base64.DEFAULT)) + "\n", false);
			
			//End data section of structure
		    currentSession.endData();
		    currentSession.noError();
		
		}
		catch (Exception e)
		{
			currentSession.endData();
			currentSession.error(e.getMessage());
		}
		finally
		{
			//Close file
			if (in != null)
			{
				try
				{
					in.close(); 
				}
				catch (Exception e) {}
			}
		     
		     //End transmission
		     currentSession.endResponse();
		     currentSession.endTransmission();
		}
	}
	
	public static void upload(List<ArgumentWrapper> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		byte[] data = Common.getParam(argsArray, "data");
		
		File file = new File(path);
		BufferedOutputStream out = null;
		
		try
		{
			out = new BufferedOutputStream(new FileOutputStream(file,true)); 
			out.write(data);
			
			currentSession.sendFullTransmission("", "");
		
		}
		catch (Exception e)
		{
			currentSession.sendFullTransmission("", e.getMessage());
		}
		finally
		{
			//Close file
			if (out != null)
			{
				try
				{
					out.close(); 
				}
				catch (Exception e) {}
			}
		}
	}
	
	public static void strings(List<ArgumentWrapper> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		
		ArrayList<String> lines = Common.strings(path);
		Iterator<String> it = lines.iterator();
		
		currentSession.startTransmission();
		currentSession.startResponse();
		currentSession.startData();
		
		while (it.hasNext())
			currentSession.send(it.next() + "\n", true); //Send this with newline
		
		currentSession.endData();
		currentSession.noError();
		currentSession.endResponse();
		currentSession.endTransmission();
	}
	
	public static void unzip(List<ArgumentWrapper> argsArray, Session currentSession){
		//Get path from arguments
		String filename = Common.getParamString(argsArray, "filename");
		String path = Common.getParamString(argsArray, "path");
		String destination = Common.getParamString(argsArray, "destination");
		
		//Unzip file
		boolean success = Common.unzipFile(filename, path, destination);
		
		if (success)
			currentSession.sendFullTransmission("", "");
		else
			currentSession.sendFullTransmission("", "Unzip failed");
	}
	
	public static void delete(List<ArgumentWrapper> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		
		try
		{
			if (new File(path).delete())
				currentSession.sendFullTransmission("", "");
			else
				currentSession.sendFullTransmission("", "Could not delete");
		}
		catch (Exception e)
		{
			currentSession.sendFullTransmission("", e.getMessage());
		}
	}

}
