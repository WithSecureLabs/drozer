// License: Refer to the README in the root directory

package com.mwr.mercury;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.Serializable;
import java.math.BigInteger;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import android.content.ComponentName;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.util.Log;

//A class to wrap arguments in
class ArgumentWrapper
{
	public String type;
	public byte[] value;
}

//An interface to use in CommandWrapper to better define Commands
interface Executor { public void execute(List<ArgumentWrapper> argsArray, Session currentSession); }

//A class to wrap commands and their implementations inside
class CommandWrapper
{
	public String section;
	public String function;
	public Executor executor;
	
	public CommandWrapper(String inputSection, String inputFunction, Executor inputExecutor)
	{
		section = inputSection;
		function = inputFunction;
		executor = inputExecutor;
	}
}

//A class to wrap requests that come in
class RequestWrapper
{
	public String section;
	public String function;
	public List<ArgumentWrapper> argsArray;
}

public class Common
{	
	
	//Mercury persistent shell
	public static Shell mercuryShell = null;
	
	//Get all local IP addresses - needs INTERNET permission
	public static ArrayList<String> getLocalIpAddresses()
	{		
		
		ArrayList<String> ips = new ArrayList<String>();
		
	    try
	    {
	    	//Iterate over all network interfaces
	        for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces(); en.hasMoreElements();)
	        {
	        	//Get next network interface
	            NetworkInterface intf = en.nextElement();
	            
	            //Iterate over all IP addresses
	            for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();)
	            {
	            	//Get next IP address
	                InetAddress inetAddress = enumIpAddr.nextElement();
	                
	                //Add IP address if it is not a loopback address
	                if (!inetAddress.isLoopbackAddress())
	                	ips.add(inetAddress.getHostAddress().toString());
	                    
	            }
	        }
	        
	    }
	    catch (SocketException ex)
	    {
	        Log.e("getLocalIpAddress", ex.toString());
	    }
	    
	    return ips;
	}
	
	//Get md5Sum of file
	public static String md5SumFile(String path)
	{
		String md5 = "";
		
		try
		{
			MessageDigest digest = MessageDigest.getInstance("MD5");
			InputStream is = new FileInputStream(new File(path));				
			byte[] buffer = new byte[8192];
			int read = 0;
			try
			{
				while( (read = is.read(buffer)) > 0)
				{
					digest.update(buffer, 0, read);
				}	
				
				byte[] md5sum = digest.digest();
				BigInteger bigInt = new BigInteger(1, md5sum);
				md5 = bigInt.toString(16);
			}
			catch(IOException e)
			{
				throw new RuntimeException("Unable to process file for MD5", e);
			}
			finally
			{
				try
				{
					is.close();
				}
				catch(IOException e) {}
			}	
		}
		catch (Exception e) {}
		
		return md5;
	}
	
	//Get parameter from a List<ArgumentWrapper> in byte[] format
	public static byte[] getParam(List<ArgumentWrapper> argWrapper, String type)
	{
		
		for (int i = 0; i < argWrapper.size(); i++)
		{
			if (argWrapper.get(i).type.toUpperCase().equals(type.toUpperCase()))
				return argWrapper.get(i).value;
		}
		
		return null;
	}
	
	//Get parameter from a List<ArgumentWrapper> in String format
	public static String getParamString(List<ArgumentWrapper> argWrapper, String type)
	{
		
		for (int i = 0; i < argWrapper.size(); i++)
		{
			if (argWrapper.get(i).type.toUpperCase().equals(type.toUpperCase()))
				return new String(argWrapper.get(i).value);
		}
		
		return "";
	}
	
	//Get parameter from a List<ArgumentWrapper> in List<String> format
	public static List<String> getParamStringList(List<ArgumentWrapper> argWrapper, String type)
	{
		List<String> returnValues = new ArrayList<String>();
		
		for (int i = 0; i < argWrapper.size(); i++)
		{
			if (argWrapper.get(i).type.toUpperCase().equals(type.toUpperCase()))
				returnValues.add(new String(argWrapper.get(i).value));
		}
		
		return returnValues;
	}

	
	//Convert a List to a contentvalues structure by splitting by =
	public static ContentValues listToContentValues(List<String> values, String type)
	{
		ContentValues contentvalues = new ContentValues();
	    
	    //Place values into contentvalue structure
	    for (int i = 0; i < values.size(); i++)
	    {
	    	String current = values.get(i);
	    	
	    	try
	    	{    	
		    	//Separate the value by = in order to get key:value
		    	Integer indexOfEquals = current.indexOf("=");
		    	String key = current.substring(0, indexOfEquals);
		    	String value = current.substring(indexOfEquals + 1);
		
		    	if (type.toUpperCase().equals("STRING"))
		    		contentvalues.put(key, value);
		    	
		    	if (type.toUpperCase().equals("BOOLEAN"))
		    		contentvalues.put(key, Boolean.valueOf(value));
	
		    	if (type.toUpperCase().equals("INTEGER"))
		    		contentvalues.put(key, new Integer(value));
		    	
		    	if (type.toUpperCase().equals("DOUBLE"))
		    		contentvalues.put(key, new Double(value));
		    	
		    	if (type.toUpperCase().equals("FLOAT"))
		    		contentvalues.put(key, new Float(value));
		    	
		    	if (type.toUpperCase().equals("LONG"))
		    		contentvalues.put(key, new Long(value));
		    	
		    	if (type.toUpperCase().equals("SHORT"))
		    		contentvalues.put(key, new Short(value));
	    	}
	    	catch (Exception e) 
	    	{
	    		Log.e("mercury", "Error with argument " + current);
	    	}
	    	
	    }
	    
	    return contentvalues;
	}
	
	//Get the columns of a content provider
	public static ArrayList<String> getColumns (ContentResolver resolver, String uri, String[] projectionArray)
	{
		//String returnValue = "";
		ArrayList<String> columns = new ArrayList<String>();
		
		try
		{				
	        //Issue query
	        Cursor c = resolver.query(Uri.parse(uri), projectionArray, null, null, null);
	                    		        	
	        //Get all column names and display
	        if (c != null)
	        {
	        	String [] colNames = c.getColumnNames();
	        	
	        	//Close the cursor
	        	c.close();
	        	
	        	//String columnNamesOutput = "";
	        	for (int k = 0; k < colNames.length; k++)
	        		columns.add(colNames[k]);
	        }
		}
		catch (Throwable t) {}
		
		return columns;
		

	}
	
	static {
		System.loadLibrary("mstring");
	}
	
	private static native String native_strings(String path);
	
	public static ArrayList<String> strings(String path) {
		ArrayList<String> lines = new ArrayList<String>();
		
		String nativeList = native_strings(path);
		
		if (nativeList != null) {		
			String[] stringList = nativeList.split("\n");
				
			if (stringList != null) {		
				for (String uri : stringList) {
					lines.add(uri);
				}
			}
		}
		
		return lines;
	}
			
	//Parse a generic intent and add to given intent
	public static Intent parseIntentGeneric(List<ArgumentWrapper> argsArray, Intent intent)
	{		
		Intent localIntent = intent;
		Iterator<ArgumentWrapper> it = argsArray.iterator();
		
		//Iterate through arguments
		while (it.hasNext())
		{
			ArgumentWrapper arg = it.next();
			
			String key = "";
			String value = "";
			
			try
			{
			
				//Try split value into key:value pair
				try
				{
					String[] split = new String(arg.value).split("=");
					key = split[0];
					value = split[1];
				}
				catch (Exception e) {}
				
				//Parse arguments into Intent
				if (arg.type.toUpperCase().equals("ACTION"))
					localIntent.setAction(new String(arg.value));
				
				if (arg.type.toUpperCase().equals("DATA"))
					localIntent.setData(Uri.parse(new String(arg.value)));
					
				if (arg.type.toUpperCase().equals("MIME_TYPE"))
					localIntent.setType(new String(arg.value));

				if (arg.type.toUpperCase().equals("CATEGORY"))
					localIntent.addCategory(new String(arg.value));
					
				if (arg.type.toUpperCase().equals("COMPONENT"))
					localIntent.setComponent(new ComponentName(key, value));
					
				if (arg.type.toUpperCase().equals("FLAGS"))
					localIntent.setFlags(Integer.parseInt(new String(arg.value)));
					
				if (arg.type.toUpperCase().equals("EXTRA-BOOLEAN"))
					localIntent.putExtra(key, Boolean.parseBoolean(value));
					
				if (arg.type.toUpperCase().equals("EXTRA-BYTE"))
					localIntent.putExtra(key, Byte.parseByte(value));
					
				if (arg.type.toUpperCase().equals("EXTRA-DOUBLE"))
					localIntent.putExtra(key, Double.parseDouble(value));
					
				if (arg.type.toUpperCase().equals("EXTRA-FLOAT"))
					localIntent.putExtra(key, Float.parseFloat(value));
					
				if (arg.type.toUpperCase().equals("EXTRA-INTEGER"))
					localIntent.putExtra(key, Integer.parseInt(value));
					
				if (arg.type.toUpperCase().equals("EXTRA-LONG"))
					localIntent.putExtra(key, Long.parseLong(value));
					
				if (arg.type.toUpperCase().equals("EXTRA-SERIALIZABLE"))
					localIntent.putExtra(key, Serializable.class.cast(value));
					
				if (arg.type.toUpperCase().equals("EXTRA-SHORT"))
					localIntent.putExtra(key, Short.parseShort(value));
					
				if (arg.type.toUpperCase().equals("EXTRA-STRING"))
					localIntent.putExtra(key, value);
					
			}
			catch (Exception e)
			{
				Log.e("mercury", "Error with argument " + arg.type + "--" + new String(arg.value));
			}
			
			
		}
		
		return localIntent;
	}

	//Extract the src file to dest - return success
	public static boolean unzipClassesDex(String src, String dest)
	{
		final int BUFFER_SIZE = 4096;
		boolean success = false;
		  
		BufferedOutputStream bufferedOutputStream = null;
		FileInputStream fileInputStream;
		try
		{
			fileInputStream = new FileInputStream(src);
			ZipInputStream zipInputStream = new ZipInputStream(new BufferedInputStream(fileInputStream));
			ZipEntry zipEntry;
		      
			while ((zipEntry = zipInputStream.getNextEntry()) != null)
			{
				String zipEntryName = zipEntry.getName();
				if (zipEntryName.toUpperCase().equals("CLASSES.DEX"))
				{
					File file = new File(dest + zipEntryName);
					byte buffer[] = new byte[BUFFER_SIZE];
					FileOutputStream fileOutputStream = new FileOutputStream(file);
					bufferedOutputStream = new BufferedOutputStream(fileOutputStream, BUFFER_SIZE);
					int count;

					while ((count = zipInputStream.read(buffer, 0, BUFFER_SIZE)) != -1)
					{
						bufferedOutputStream.write(buffer, 0, count);
					}

					bufferedOutputStream.flush();
					bufferedOutputStream.close();
					
					success = true;
				}

			}
			zipInputStream.close();
		}
		catch (Exception e)
		{
			Log.e("mercury", e.getMessage());
		}

			   
		return success;

	}


}
