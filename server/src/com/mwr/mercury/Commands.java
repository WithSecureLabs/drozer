// License: Refer to the README in the root directory

package com.mwr.mercury;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import android.content.ComponentName;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.PathPermission;
import android.content.pm.ProviderInfo;
import android.content.pm.ResolveInfo;
import android.content.pm.ServiceInfo;
import android.database.Cursor;
import android.net.Uri;
import android.os.PatternMatcher;
import android.util.Base64;

public class Commands
{

	public static final ArrayList<CommandWrapper> commandList;
	
	static
	{
		//Initialise list of commands
		commandList = new ArrayList<CommandWrapper>();
		
		
		/*************************************************************************************/
		/** Command section - CORE
		/*************************************************************************************/
		
		//core.ping() - returns "pong"
		commandList.add(new CommandWrapper("core", "ping", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				currentSession.sendFullTransmission("pong", "");
			}
		}));
		
		//core.version() - returns Mercury version
		commandList.add(new CommandWrapper("core", "version", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				String version = "";
				try
				{
					version = currentSession.applicationContext.getPackageManager().getPackageInfo(currentSession.applicationContext.getPackageName(), 0).versionName;
				}
				catch (Exception e) {}
				currentSession.sendFullTransmission(version, "");
			}
		}));
		
		//core.fileSize(path) - returns size of file in bytes
		commandList.add(new CommandWrapper("core", "fileSize", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
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
		}));
		
		//core.fileMD5(path) - returns md5sum of file
		commandList.add(new CommandWrapper("core", "fileMD5", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
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
		}));
		
		//core.download(path) - send the contents of the file
		commandList.add(new CommandWrapper("core", "download", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
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
		}));
		
		//core.upload(path) - receive a part of a file and append to file found @ path
		commandList.add(new CommandWrapper("core", "upload", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
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
		}));
		
		//core.delete(path) - returns nothing in <data> if file was delete else return <error>
		commandList.add(new CommandWrapper("core", "delete", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
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
		}));
		
		//core.strings(path) - returns a list of readable chars in a file
		commandList.add(new CommandWrapper("core", "strings", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
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
		}));
		
		
		//core.unzip(path, destination) - places unzipped file in destinationFolder
		commandList.add(new CommandWrapper("core", "unzip", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Get path from arguments
				String path = Common.getParamString(argsArray, "path");
				String destination = Common.getParamString(argsArray, "destination");
				
				//Unzip file
				boolean success = Common.unzipClassesDex(path, destination);
				
				if (success)
					currentSession.sendFullTransmission("", "");
				else
					currentSession.sendFullTransmission("", "Unzip failed");
				
			}
		}));
		
		
		
		/*************************************************************************************/
		/** Command section - DEBUGGABLE
		/*************************************************************************************/
		
		//debuggable.info(path) - return info on debuggable apps
		commandList.add(new CommandWrapper("debuggable", "info", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Assign filter if one came in the arguments
				String filter = Common.getParamString(argsArray, "filter");
				
				//String to return at the end of function
				String returnValue = "";
				
				//Get all packages from packagemanager
				List <PackageInfo> packages = currentSession.applicationContext.getPackageManager().getInstalledPackages(0);
				
				//Iterate through packages
				for (PackageInfo package_:packages)
				{
					ApplicationInfo app = package_.applicationInfo;
					
					//Focus on debuggable apps only and apply filter
					if (((app.flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0) && (app.packageName.contains(filter) || app.processName.contains(filter) || filter == ""))
		            {
						returnValue += "Package name: " + app.packageName + "\n";
						returnValue += "UID: " + app.uid + "\n";
						
		            	//Find all permissions that this app has
		            	String strPermissions = "";
		            	String[] permissions = package_.requestedPermissions;
		            	
		            	if (permissions != null)
		            	{
		            		for (String permission:permissions)
		            			strPermissions += permission + "; ";
		            	}
		            	
		            	returnValue += "Permissions: " + strPermissions + "\n\n";
		            }
				}
				
				currentSession.sendFullTransmission(returnValue.trim(), "");
			}
		}));
		
		
		
		/*************************************************************************************/
		/** Command section - ACTIVITY
		/*************************************************************************************/
		
		//activity.info(filter) - returns info on exported activities
		commandList.add(new CommandWrapper("activity", "info", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Assign filter if one came in the arguments
				String filter = Common.getParamString(argsArray, "filter");
				
				currentSession.startTransmission();
				currentSession.startResponse();
				currentSession.startData();
				
				//Iterate through all packages
				List<PackageInfo> packages = currentSession.applicationContext.getPackageManager().getInstalledPackages(0);
		        for(PackageInfo pack : packages)
		        {
		        	//Get activities in package
		            ActivityInfo[] activities = null;
		            try
		            {
		            	activities = currentSession.applicationContext.getPackageManager().getPackageInfo(pack.packageName, PackageManager.GET_ACTIVITIES).activities;
		            }
		            catch (Exception e) {}
		            
	            	if (activities != null)
					{	
						for (int i = 0; i < activities.length; i++)
						{
							if (activities[i].exported == true)
							{
								boolean filterPresent = filter.length() != 0;
								boolean filterRelevant = pack.packageName.contains(filter) || activities[i].name.contains(filter);
								
								if ((filterPresent && filterRelevant) || !filterPresent)
								{
									currentSession.send("Package name: " + activities[i].packageName + "\n", true);
									currentSession.send("Activity: " + activities[i].name + "\n\n", true);
								}
							}
						}
					}
		        }
				
				currentSession.endData();
				currentSession.noError();
				currentSession.endResponse();
				currentSession.endTransmission();
				
			}
		}));
		
		//activity.start(args from parseIntentGeneric) - returns success of starting activity
		commandList.add(new CommandWrapper("activity", "start", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Parse intent
				Intent intent = Common.parseIntentGeneric(argsArray, new Intent());
				
				try
				{
					currentSession.applicationContext.startActivity(intent);
					currentSession.sendFullTransmission("Activity started with " + intent.toString(), "");
				}
				catch (Throwable t)
				{
					currentSession.sendFullTransmission("", t.getMessage());
				}
				
			}
		}));
		
		//activity.match(args from parseIntentGeneric) - return the apps that match the given intent
		commandList.add(new CommandWrapper("activity", "match", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Parse intent
				Intent intent = Common.parseIntentGeneric(argsArray, new Intent());

				try
				{
				
					//Get all activities and iterate through them
					List<ResolveInfo> activities = currentSession.applicationContext.getPackageManager().queryIntentActivities(intent, PackageManager.MATCH_DEFAULT_ONLY & PackageManager.GET_ACTIVITIES & PackageManager.GET_INTENT_FILTERS & PackageManager.GET_RESOLVED_FILTER	);
	
					String returnVal = intent.toString() + ":\n\n";
					
					for (int i = 0; i < activities.size(); i++)
					{
	
						String activityPackage = activities.get(i).activityInfo.packageName;
						String activityTargetActivity = activities.get(i).activityInfo.name;
	
						returnVal += "Package name: " + activityPackage + "\n";
						returnVal += "Target activity: " + activityTargetActivity + "\n\n";
	
					}
					
					currentSession.sendFullTransmission(returnVal.trim(), "");
				
				}
				catch (Exception e)
				{
					currentSession.sendFullTransmission("", e.getMessage());
				}
				
			}
		}));
		
		//activity.launchintent(packageName) - returns the intent that can be used to launch the app
		commandList.add(new CommandWrapper("activity", "launchintent", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Assign filter if one came in the arguments
				String packageName = Common.getParamString(argsArray, "packageName");
				
				Intent intent = currentSession.applicationContext.getPackageManager().getLaunchIntentForPackage(packageName);
				
				//Send intent back
				if (intent != null)
					currentSession.sendFullTransmission(intent.toString(), "");
				else
					currentSession.sendFullTransmission("", "No intent returned	");
				
			}
		}));
		
		
		
		/*************************************************************************************/
		/** Command section - BROADCAST
		/*************************************************************************************/
		
		//broadcast.info(filter) - returns info on exported broadcast receivers
		commandList.add(new CommandWrapper("broadcast", "info", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Assign filter if one came in the arguments
				String filter = Common.getParamString(argsArray, "filter");
				
				currentSession.startTransmission();
				currentSession.startResponse();
				currentSession.startData();
				
				//Get all packages from packagemanager
				PackageManager pm = currentSession.applicationContext.getPackageManager();
				List <PackageInfo> packages = pm.getInstalledPackages(PackageManager.GET_RECEIVERS | PackageManager.GET_PERMISSIONS);
				
				//Iterate through packages
				for (PackageInfo package_:packages)
				{
					
					ActivityInfo[] receivers = package_.receivers;			
					
					if (receivers != null)
					{	
						for (int i = 0; i < receivers.length; i++)
						{
							if (receivers[i].exported == true)
							{
								boolean filterPresent = filter.length() != 0;
								boolean filterRelevant = package_.packageName.contains(filter) || receivers[i].name.contains(filter);
								
								if ((filterPresent && filterRelevant) || !filterPresent)
								{
									currentSession.send("Package name: " + receivers[i].packageName + "\n", true);
									currentSession.send("Receiver: " + receivers[i].name + "\n\n", true);
								}
							}
						}
					}
				}
				
				currentSession.endData();
				currentSession.noError();
				currentSession.endResponse();
				currentSession.endTransmission();
				
			}
		}));
		
		//broadcast.start(args from parseIntentGeneric) - returns success of sending broadcast
		commandList.add(new CommandWrapper("broadcast", "send", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Parse intent
				Intent intent = Common.parseIntentGeneric(argsArray, new Intent());
				
				try
				{
					currentSession.applicationContext.sendBroadcast(intent);
					currentSession.sendFullTransmission("Broadcast sent with " + intent.toString(), "");
				}
				catch (Throwable t)
				{
					currentSession.sendFullTransmission("", t.getMessage());
				}
				
			}
		}));
		
		
		/*************************************************************************************/
		/** Command section - SERVICE
		/*************************************************************************************/
		
		//service.info(filter) - returns info on exported services
		commandList.add(new CommandWrapper("service", "info", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Assign filter and permissions if they came in the arguments
				String filter = Common.getParamString(argsArray, "filter");
				String permissions = Common.getParamString(argsArray, "permissions");
				
				currentSession.startTransmission();
				currentSession.startResponse();
				currentSession.startData();
				
				//Get all packages from packagemanager
				PackageManager pm = currentSession.applicationContext.getPackageManager();
				List <PackageInfo> packages = pm.getInstalledPackages(PackageManager.GET_SERVICES | PackageManager.GET_PERMISSIONS);
				
				//Iterate through packages
				for (PackageInfo package_:packages)
				{
					ServiceInfo[] services = package_.services;			
					
					if (services != null)
					{	
						for (int i = 0; i < services.length; i++)
						{							
							boolean relevantFilter = false;
							boolean relevantPermissions = false;
							boolean noFilters = false;
							boolean bothFiltersRelevant = false;
							
							//Check if a filter was used
							if (filter.length() > 0)
								relevantFilter = package_.packageName.contains(filter) || services[i].name.contains(filter);
							
							//Check if a permission filter was used
							try
							{
								if (permissions.length() > 0)
								{
									if (permissions.toUpperCase().equals("NULL"))
										relevantPermissions = (services[i].permission == null);
									else
										relevantPermissions = services[i].permission.contains(permissions);
								}
							} catch (Throwable t) {}
							
							//Check if no parameters were given
							if (filter.length() == 0 && permissions.length() == 0)
								noFilters = true;
							
							boolean bothFiltersPresent = false;
							if ((filter != "") && (permissions != ""))
								bothFiltersPresent = true;
							
							if (bothFiltersPresent && relevantFilter && relevantPermissions)
								bothFiltersRelevant = true;
							
							//Apply filter and only look @ exported providers
							if (((bothFiltersPresent && bothFiltersRelevant) || (!bothFiltersPresent && (relevantFilter || relevantPermissions)) || (!bothFiltersPresent && noFilters)) && services[i].exported)
							{
								currentSession.send("Package name: " + services[i].packageName + "\n", true);
								currentSession.send("Service: " + services[i].name + "\n", true);
								currentSession.send("Required Permission: " + services[i].permission + "\n\n", true);
							}
						}
					}
				}
				
				currentSession.endData();
				currentSession.noError();
				currentSession.endResponse();
				currentSession.endTransmission();
				
			}
		}));
		
		//service.start(args from parseIntentGeneric) - returns success of starting service
		commandList.add(new CommandWrapper("service", "start", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Parse intent
				Intent intent = Common.parseIntentGeneric(argsArray, new Intent());
				
				try
				{
					ComponentName service = currentSession.applicationContext.startService(intent);
					currentSession.sendFullTransmission("Service started with " + intent.toString() + " - " + service.flattenToString(), "");
				}
				catch (Throwable t)
				{
					currentSession.sendFullTransmission("", t.getMessage());
				}
				
			}
		}));
		
		//service.stop(args from parseIntentGeneric) - returns success of stoping service
		commandList.add(new CommandWrapper("service", "stop", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Parse intent
				Intent intent = Common.parseIntentGeneric(argsArray, new Intent());
				
				try
				{
					boolean stopped = currentSession.applicationContext.stopService(intent);
					if (stopped)
						currentSession.sendFullTransmission("Service stopped with " + intent.toString(), "");
					else
						currentSession.sendFullTransmission("Stopping service failed", "");
				}
				catch (Throwable t)
				{
					currentSession.sendFullTransmission("", t.getMessage());
				}
				
			}
		}));
		
		
		/*************************************************************************************/
		/** Command section - PROVIDER
		/*************************************************************************************/
		
		//provider.info(filter, permissions) - returns info on content providers
		commandList.add(new CommandWrapper("provider", "info", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Assign filter and permissions if they came in the arguments	
				String filter = Common.getParamString(argsArray, "filter");
				String permissions = Common.getParamString(argsArray, "permissions");
				
				currentSession.startTransmission();
				currentSession.startResponse();
				currentSession.startData();
				
				//Get all providers and iterate through them
				List<ProviderInfo> providers = currentSession.applicationContext.getPackageManager().queryContentProviders(null, PackageManager.GET_URI_PERMISSION_PATTERNS, PackageManager.GET_URI_PERMISSION_PATTERNS);
				
				//Iterate through content providers
				for (int i = 0; i < providers.size(); i++)
				{
					//Get all relevant info from content provider
					String providerAuthority = providers.get(i).authority;
					String providerPackage = providers.get(i).packageName;
					String providerReadPermission = providers.get(i).readPermission;
					PatternMatcher[] uriPermissionPatterns = providers.get(i).uriPermissionPatterns;
					String providerWritePermission = providers.get(i).writePermission;
					PathPermission[] providerPathPermissions = providers.get(i).pathPermissions;
					boolean providerMultiprocess = providers.get(i).multiprocess;
					boolean grantUriPermissions = providers.get(i).grantUriPermissions;
					
					String pathpermissions = "";
					
					//Path permissions
					if (providerPathPermissions != null)
						for (int j = 0; j < providerPathPermissions.length; j++)
						{
							if (providerPathPermissions[j].getReadPermission() != null)
								pathpermissions += "Path Permission - Read: " + providerPathPermissions[j].getPath() + " needs " + providerPathPermissions[j].getReadPermission() + "\n";

							if (providerPathPermissions[j].getWritePermission() != null)
								pathpermissions += "Path Permission - Write: " + providerPathPermissions[j].getPath() + " needs " + providerPathPermissions[j].getWritePermission() + "\n";
						}
					
					String uriPermissions = "";
					
					//URI Permission Patterns
					if (uriPermissionPatterns != null)
						for (int k = 0; k < uriPermissionPatterns.length; k++)
						{
							if (uriPermissionPatterns[k].getPath() != null)
								uriPermissions += "URI Permission Pattern: " + uriPermissionPatterns[k].getPath() + "\n";
							
						}

					boolean relevantFilter = false;
					boolean relevantPermissions = false;
					boolean noFilters = false;
					boolean bothFiltersRelevant = false;
					
					//Check if a filter was used
					if (filter.length() > 0)
						relevantFilter = providerAuthority.toUpperCase().contains(filter.toUpperCase()) || providerPackage.toUpperCase().contains(filter.toUpperCase());
					
					//Check if a permission filter was used
					try
					{
						if (permissions.length() > 0)
						{
							if (permissions.toUpperCase().equals("NULL"))
								relevantPermissions = (providerReadPermission == null) || (providerWritePermission == null);
							else
								relevantPermissions = providerReadPermission.contains(permissions) || providerWritePermission.contains(permissions);
						}
					} catch (Throwable t) {}
					
					//Check if no parameters were given
					if (filter.length() == 0 && permissions.length() == 0)
						noFilters = true;
					
					boolean bothFiltersPresent = false;
					if ((filter != "") && (permissions != ""))
						bothFiltersPresent = true;
					
					if (bothFiltersPresent && relevantFilter && relevantPermissions)
						bothFiltersRelevant = true;
					
					//Apply filter and only look @ exported providers
					if (((bothFiltersPresent && bothFiltersRelevant) || (!bothFiltersPresent && (relevantFilter || relevantPermissions)) || (!bothFiltersPresent && noFilters)) && providers.get(i).exported)
					{
						currentSession.send("Package name: " + providerPackage + "\n", true);
						currentSession.send("Authority: " + providerAuthority + "\n", true);
						currentSession.send("Required Permission - Read: " + providerReadPermission + "\n", true);
						currentSession.send("Required Permission - Write: " + providerWritePermission + "\n", true);
						currentSession.send((pathpermissions.length() > 0)? pathpermissions: "", true);
						currentSession.send((uriPermissions.length() > 0)? uriPermissions: "", true);
						currentSession.send("Grant Uri Permissions: " + grantUriPermissions + "\n", true);
						currentSession.send("Multiprocess allowed: " + providerMultiprocess + "\n\n", true);
					}

				}
				
				currentSession.endData();
				currentSession.noError();
				currentSession.endResponse();
				currentSession.endTransmission();		

			}
		}));
		
		
		//provider.columns(uri) - returns the columns on a content provider
		commandList.add(new CommandWrapper("provider", "columns", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Get list of columns
				ArrayList<String> columns = Common.getColumns(currentSession.applicationContext.getContentResolver(), new String(Common.getParam(argsArray, "uri")), null);
				
				//If there are no columns, then the URI is invalid
				if (columns.size() == 0)
					currentSession.sendFullTransmission("", "Invalid content URI specified");
				else
				{
					String columnsStr = "";
					
					//Iterate through columns
					for (int i = 0; i < columns.size(); i++)
					{
						if (i != columns.size() - 1)
							columnsStr += columns.get(i) + " | ";
						else
							columnsStr += columns.get(i);
					}
        	
					currentSession.sendFullTransmission(columnsStr, "");
				}
			
			}
		}));
		
		//provider.query(uri) - returns the query
		commandList.add(new CommandWrapper("provider", "query", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				currentSession.startTransmission();
				currentSession.startResponse();
				currentSession.startData();
				
				try
				{				
					//Get content provider and cursor
			        ContentResolver r = currentSession.applicationContext.getContentResolver();
			        
			        //Get all the parameters
			        List<String> projection = Common.getParamStringList(argsArray, "projection");
			        String selection = Common.getParamString(argsArray, "selection");
			        List<String> selectionArgs = Common.getParamStringList(argsArray, "selectionArgs");
			        String sortOrder = Common.getParamString(argsArray, "sortOrder");
			        String showColumns = Common.getParamString(argsArray, "showColumns");
			        
			        //Put projection in an array
			        String[] projectionArray = null;
			        if (projection.size() > 0)
			        {
			        	projectionArray = new String[projection.size()];
			        	Iterator<String> it = projection.iterator();
			        	
			        	int i = 0;
			        	
			        	while (it.hasNext())
			        	{
			        		projectionArray[i] = it.next();
			        		i++;
			        	}
			        }
			        
			        //Put selectionArgs in an array
					String[] selectionArgsArray = null;
					if (selectionArgs.size() > 0)
					{
						selectionArgsArray = new String[selectionArgs.size()];
						Iterator<String> it = selectionArgs.iterator();
						
						int i = 0;
						
						while (it.hasNext())
						{
							selectionArgsArray[i] = it.next();
							i++;
						}
					}
			        
			        //Issue query
			        Cursor c = r.query(Uri.parse(new String(Common.getParam(argsArray, "Uri"))), projectionArray, (selection.length() > 0)? selection : null, selectionArgsArray, (sortOrder.length() > 0)? sortOrder : null);
			        
			        //Check if query failed
			        if (c != null)
			        {
				        //Display the columns
				        if (showColumns.length() == 0 || showColumns.toUpperCase().contains("TRUE"))
				        {
				        	ArrayList<String> cols = Common.getColumns(r, Common.getParamString(argsArray, "Uri"), projectionArray);
				        	Iterator<String> it = cols.iterator();
				        	String columns = "";
				        	
				        	while (it.hasNext())
				        		columns += it.next() + " | ";
				 
				        	currentSession.send(columns.substring(0, columns.length()-3), true);
				        	currentSession.send("\n.....\n\n", true);
				        }
				        	
			        	//Get all rows of data
			        	for (c.moveToFirst();!c.isAfterLast();c.moveToNext())
			        	{	
			        		int numOfColumns = c.getColumnCount();
			        		String data = "";
			        		
			        		//Iterate through columns
			        		for (int l = 0; l < numOfColumns; l++)
			        		{
			        			
			        			//Get string - if there is an error try retrieve as a blob
			        			try
			        			{
			        				data += c.getString(l);
			        			}
			        			catch (Exception e)
			        			{
			        				//Base64 encode blobs and prepend with (blob)
			        				data += "(blob) " + Base64.encodeToString(c.getBlob(l), Base64.DEFAULT);
			        			}
			        			
			        			//Check if a column separator should be added or not
			        			if (l != (numOfColumns - 1))
			        				data += " | ";
			        		}
	
			        		currentSession.send(data + "\n\n", true);
			        	}
			        	
			        	currentSession.endData();
			        	currentSession.noError();
			        }
			        else
			        {
			        	currentSession.endData();
						currentSession.error("Query failed");
			        }
		        
				}
				catch (Throwable t) 
				{
					currentSession.endData();
					currentSession.error(t.getMessage());
				}
				
				currentSession.endResponse();
				currentSession.endTransmission();
			
			}
		}));
		
		
		//provider.read(Uri) - implements openInputStream and reads - returns file contents
        commandList.add(new CommandWrapper("provider", "read", new Executor()
        {
              
        public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
        {
        	
        	//Start transmission
        	currentSession.startTransmission();
        	currentSession.startResponse();
        	currentSession.startData();
        	
            try
            {
                Uri uri = Uri.parse(Common.getParamString(argsArray, "Uri"));
                ContentResolver r = currentSession.applicationContext.getContentResolver();
                InputStream is = r.openInputStream(uri);
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                int len = -1;
                do
                {
                    byte[] buf = new byte[1024];
                    len = is.read(buf);
                    if (len > 0)
                    	baos.write(buf, 0, len);
                    
                } while(len != -1);
                
                byte[] buf = baos.toByteArray();
                String b64 = Base64.encodeToString(buf, 0);
                
                //Send response
                currentSession.send(b64, false);
                currentSession.endData();
            	currentSession.noError();
            }
            catch (Throwable t)
            {
            	currentSession.endData();
            	currentSession.error(t.getMessage());
            }
        	finally
        	{
        		currentSession.endResponse();
        		currentSession.endTransmission();
        	}
        	
        	
    	}
    }));
		
		
		
		//provider.insert(many args parsed by Common.listToContentValues) - returns uri string
		commandList.add(new CommandWrapper("provider", "insert", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				try
				{					        
			        ContentValues contentvalues = new ContentValues();
			        
			        //Place values into contentvalue structure
			        List<String> strings = Common.getParamStringList(argsArray, "string");
			        if (strings != null)
				        contentvalues.putAll(Common.listToContentValues(strings, "string"));
			        
			        List<String> booleans = Common.getParamStringList(argsArray, "boolean");
			        if (booleans != null)
				        contentvalues.putAll(Common.listToContentValues(booleans, "boolean"));
			        
			        List<String> integers = Common.getParamStringList(argsArray, "integer");
			        if (integers != null)
				        contentvalues.putAll(Common.listToContentValues(integers, "integer"));
			        
			        List<String> doubles = Common.getParamStringList(argsArray, "double");
			        if (doubles != null)
				        contentvalues.putAll(Common.listToContentValues(doubles, "double"));
			        
			        List<String> floats = Common.getParamStringList(argsArray, "float");
			        if (floats != null)
				        contentvalues.putAll(Common.listToContentValues(floats, "float"));
			        
			        List<String> longs = Common.getParamStringList(argsArray, "long");
			        if (longs != null)
				        contentvalues.putAll(Common.listToContentValues(longs, "long"));
			        
			        List<String> shorts = Common.getParamStringList(argsArray, "short");
			        if (shorts != null)
				        contentvalues.putAll(Common.listToContentValues(shorts, "short"));

			        //Get content resolver
			        ContentResolver r = currentSession.applicationContext.getContentResolver();
			        
			        //Issue insert command
			        Uri c = r.insert(Uri.parse(new String(Common.getParam(argsArray, "Uri"))), contentvalues);
			       
			        currentSession.sendFullTransmission(c.toString(), "");
		        
				}
				catch (Throwable t) 
				{
					currentSession.sendFullTransmission("", t.getMessage());
				}
				
			}
		}));
		
		//provider.update(many args parsed by Common.listToContentValues) - returns number of affected rows in string
		commandList.add(new CommandWrapper("provider", "update", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				try
				{					        
			        ContentValues contentvalues = new ContentValues();
			        
			        //Place values into contentvalue structure
			        List<String> strings = Common.getParamStringList(argsArray, "string");
			        if (strings != null)
				        contentvalues.putAll(Common.listToContentValues(strings, "string"));
			        
			        List<String> booleans = Common.getParamStringList(argsArray, "boolean");
			        if (booleans != null)
				        contentvalues.putAll(Common.listToContentValues(booleans, "boolean"));
			        
			        List<String> integers = Common.getParamStringList(argsArray, "integer");
			        if (integers != null)
				        contentvalues.putAll(Common.listToContentValues(integers, "integer"));
			        
			        List<String> doubles = Common.getParamStringList(argsArray, "double");
			        if (doubles != null)
				        contentvalues.putAll(Common.listToContentValues(doubles, "double"));
			        
			        List<String> floats = Common.getParamStringList(argsArray, "float");
			        if (floats != null)
				        contentvalues.putAll(Common.listToContentValues(floats, "float"));
			        
			        List<String> longs = Common.getParamStringList(argsArray, "long");
			        if (longs != null)
				        contentvalues.putAll(Common.listToContentValues(longs, "long"));
			        
			        List<String> shorts = Common.getParamStringList(argsArray, "short");
			        if (shorts != null)
				        contentvalues.putAll(Common.listToContentValues(shorts, "short"));

			        List<String> selectionArgs = Common.getParamStringList(argsArray, "selectionArgs");
			        String where = Common.getParamString(argsArray, "where");

			        //Put selectionArgs in an array
					String[] selectionArgsArray = null;
					if (selectionArgs.size() > 0)
					{
						selectionArgsArray = new String[selectionArgs.size()];
						Iterator<String> it = selectionArgs.iterator();
						
						int i = 0;
						
						while (it.hasNext())
						{
							selectionArgsArray[i] = it.next();
							i++;
						}
					}
			        
			        //Get content resolver
			        ContentResolver r = currentSession.applicationContext.getContentResolver();
			        
			        //Issue update command
			        Integer c = r.update(Uri.parse(Common.getParamString(argsArray, "Uri")), contentvalues, (where.length() > 0)? where : null, selectionArgsArray);
		        
			        //Send response
			        currentSession.sendFullTransmission(c.toString() + " rows have been updated.", "");
			        
				}
				catch (Throwable t) 
				{
					currentSession.sendFullTransmission("", t.getMessage());
				}
				
			}
		}));
		
		//provider.delete(Uri) - returns number of affected rows in string
		commandList.add(new CommandWrapper("provider", "delete", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				try
				{
					
					List<String> selectionArgs = Common.getParamStringList(argsArray, "selectionArgs");
			        String where = Common.getParamString(argsArray, "where");

			        //Put selectionArgs in an array
					String[] selectionArgsArray = null;
					if (selectionArgs.size() > 0)
					{
						selectionArgsArray = new String[selectionArgs.size()];
						Iterator<String> it = selectionArgs.iterator();
						
						int i = 0;
						
						while (it.hasNext())
						{
							selectionArgsArray[i] = it.next();
							i++;
						}
					}
			        
			        //Get content resolver
			        ContentResolver r = currentSession.applicationContext.getContentResolver();

			        //Issue delete command
			        int rowsDeleted = r.delete(Uri.parse(Common.getParamString(argsArray, "Uri")), (where.length() > 0)? where : null, selectionArgsArray);
			       
			        //Send response
			        currentSession.sendFullTransmission(Integer.toString(rowsDeleted) + " rows have been deleted", "");
		        
				}
				catch (Throwable t) 
				{
					currentSession.sendFullTransmission("", t.getMessage());
				}
				
				currentSession.endTransmission();
				
			}
		}));
		
		//provider.finduri(path) - returns a list of uris in the target
		commandList.add(new CommandWrapper("provider", "finduri", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{		
				//Get path from arguments
				String path = Common.getParamString(argsArray, "path");
				
				//Get all strings from the file
				ArrayList<String> fullLines = Common.strings(path);
				
				//Filter URI 								
				ArrayList<String> lines = new ArrayList<String>();
				
				for (String line : fullLines) {
					if (line.toUpperCase().contains("CONTENT://") &&
							!line.toUpperCase().equals("CONTENT://")) {
						lines.add(line);
					}
				}
								
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
		}));
		
		
		/*************************************************************************************/
		/** Command section - PACKAGES
		/*************************************************************************************/
		
		//packages.info(filter) - return info on packages
		commandList.add(new CommandWrapper("packages", "info", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				currentSession.startTransmission();
				currentSession.startResponse();
				currentSession.startData();
				
				//Assign filter and permissions if they came in the arguments
				String filter = Common.getParamString(argsArray, "filter");
				String permissions = Common.getParamString(argsArray, "permissions");
							
				//Get all packages from packagemanager
				PackageManager pm = currentSession.applicationContext.getPackageManager();
				List <PackageInfo> packages = pm.getInstalledPackages(PackageManager.GET_PERMISSIONS|PackageManager.GET_CONFIGURATIONS|PackageManager.GET_GIDS|PackageManager.GET_SHARED_LIBRARY_FILES);
				
				//Iterate through packages
				for (PackageInfo currentPackage:packages)
				{			
					ApplicationInfo app = currentPackage.applicationInfo;
					
					String packageName = app.packageName;
					String processName = app.processName;
					String dataDir = app.dataDir;
					String publicSourceDir = app.publicSourceDir;
					Integer uid = app.uid;
					String sharedUserId = currentPackage.sharedUserId;
					int[] gids = currentPackage.gids;
					String version = currentPackage.versionName;
					String [] libraries = app.sharedLibraryFiles;
					
					//Find all permissions that this app has requested
		        	String requestedPermissions = "";
		        	String[] requestedPermissionsArray = currentPackage.requestedPermissions;
		        	
		        	if (requestedPermissionsArray != null)
		        	{
		        		for (String permission:requestedPermissionsArray)
		        			requestedPermissions += permission + "; ";
		        	}
		        	
		        	String librariesString = "";
		        	if (libraries != null)
		        		for (int i = 0; i < libraries.length; i++)
		        		librariesString += libraries[i] + "; ";
		        	
		        	//Get the GIDs
		        	String gidString = "";
		        	if (gids != null)
		        	for (int z = 0; z < gids.length; z++)
		        		gidString += new Integer(gids[z]).toString() + "; ";
		        	
					boolean relevantFilter = filter != "";
					if (relevantFilter)
						relevantFilter = packageName.toUpperCase().contains(filter.toUpperCase()) || processName.toUpperCase().contains(filter.toUpperCase()) || dataDir.toUpperCase().contains(filter.toUpperCase()) || publicSourceDir.toUpperCase().contains(filter.toUpperCase());

					boolean relevantPermissions = permissions != "";
					if (relevantPermissions)
						relevantPermissions = requestedPermissions.toUpperCase().contains(permissions.toUpperCase());
					
					boolean bothFiltersPresent = false;
					if ((filter != "") && (permissions != ""))
						bothFiltersPresent = true;
					
					boolean bothFiltersRelevant = false;
					if (bothFiltersPresent && relevantFilter && relevantPermissions)
						bothFiltersRelevant = true;
					
					boolean noFilters = (filter.length() == 0) && (permissions.length() == 0);
					
					//Apply filter
					if ((bothFiltersPresent && bothFiltersRelevant) || (!bothFiltersPresent && (relevantFilter || relevantPermissions)) || (!bothFiltersPresent && noFilters))
		            {
						currentSession.send("Package name: " + packageName + "\n", true);
						currentSession.send("Process name: " + processName + "\n", true);
						currentSession.send("Version: " + version + "\n", true);
						currentSession.send("Data directory: " + dataDir + "\n", true);
						currentSession.send("APK path: " + publicSourceDir + "\n", true);
						currentSession.send("UID: " + uid + "\n", true);
						currentSession.send("GID: " + gidString + "\n", true);
						
						if (librariesString.length() > 0)
							currentSession.send("Shared libraries: " + librariesString + "\n", true);
		            	
		            	if (sharedUserId != null)
		            		currentSession.send("SharedUserId: " + sharedUserId + " (" + uid + ")\n", true);
		            	
		            	currentSession.send("Permissions: " + requestedPermissions + "\n\n", true);
		            	
		            }
				}
			
				currentSession.endData();
				currentSession.noError();
				currentSession.endResponse();
				currentSession.endTransmission();
			}
		}));
		
		//packages.shareduid(filter) - return packages that share uid's
		commandList.add(new CommandWrapper("packages", "shareduid", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				currentSession.startTransmission();
				currentSession.startResponse();
				currentSession.startData();
				
				//Get all the parameters
				String filter = Common.getParamString(argsArray, "uid");
							
				//Get all packages from packagemanager
				PackageManager pm = currentSession.applicationContext.getPackageManager();
				List <PackageInfo> packages = pm.getInstalledPackages(PackageManager.GET_PERMISSIONS);

				List<Integer> uidList = new ArrayList<Integer>();
				
				//Get all UIDs
				for (PackageInfo package_:packages)
				{
					ApplicationInfo app = package_.applicationInfo;
					
					if (!uidList.contains(app.uid))
						uidList.add(app.uid);
				}
				
				//Iterate through packages
				for (Integer uid:uidList)
				{
					String[] packageNames = pm.getPackagesForUid(uid);
					String accumulatedPermissions = "";
								
					if ((filter.length() > 0 && filter.equals(uid.toString())) || filter.length() == 0)
					{
						currentSession.send("UID: " + uid + " (" + pm.getNameForUid(uid) + ")\n", true);
										
						if (packages != null)
						{
							for (int s = 0; s < packageNames.length; s++)
							{
								//Get package permissions and add to list of accumulated
								PackageInfo pack = null;
								
								try
								{
									pack = currentSession.applicationContext.getPackageManager().getPackageInfo(packageNames[s], PackageManager.GET_PERMISSIONS);
								}
								catch (Exception e) {}
								
								String[] requestedPermissionsArray = pack.requestedPermissions;
					        	
					        	if (requestedPermissionsArray != null)
					        	{
					        		for (String permission:requestedPermissionsArray)
					        			if (!accumulatedPermissions.contains(permission))
					        			accumulatedPermissions += permission + "; ";
					        	}
					        	
					        	currentSession.send("Package name: " + packageNames[s] + "\n", true);
							}
							
						}
						
						//Send accumulated permissions
						currentSession.send("Accumulated permissions: " + accumulatedPermissions + "\n", true);
			
						currentSession.send("\n", true);
					}
				}
			
				currentSession.endData();
				currentSession.noError();
				currentSession.endResponse();
				currentSession.endTransmission();
			}
		}));
		
		//packages.attacksurface(packageName) - return attack surface
		commandList.add(new CommandWrapper("packages", "attacksurface", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Get all the parameters
				String packageName = Common.getParamString(argsArray, "packageName");
				
				try
				{
				
					//Check number of exported activities
					int numActivities = 0;
					
					ActivityInfo[] activities = currentSession.applicationContext.getPackageManager().getPackageInfo(packageName, PackageManager.GET_ACTIVITIES).activities;
					if (activities != null)
						for (int i = 0; i < activities.length; i++)
							if (activities[i].exported)
								numActivities++;
	
					//Check number of exported receivers
					int numReceivers = 0;
					ActivityInfo[] receivers = currentSession.applicationContext.getPackageManager().getPackageInfo(packageName, PackageManager.GET_RECEIVERS).receivers;
					if (receivers != null)
						for (int i = 0; i < receivers.length; i++)
							if (receivers[i].exported)
								numReceivers++;
	
					//Check number of exported providers
					int numProviders = 0;
					ProviderInfo[] providers = currentSession.applicationContext.getPackageManager().getPackageInfo(packageName, PackageManager.GET_PROVIDERS).providers;
					if (providers != null)
						for (int i = 0; i < providers.length; i++)
							if (providers[i].exported)
								numProviders++;
	
					//Check number of exported services
					int numServices = 0;
					ServiceInfo[] services = currentSession.applicationContext.getPackageManager().getPackageInfo(packageName, PackageManager.GET_SERVICES).services;
					if (services != null)
						for (int i = 0; i < services.length; i++)
							if (services[i].exported)
								numServices++;
	
					String attackSurface = "";
					attackSurface += numActivities + " activities exported\n";
					attackSurface += numReceivers + " broadcast receivers exported\n";
					attackSurface += numProviders + " content providers exported\n";
					attackSurface += numServices + " services exported\n\n";
					
					if ((currentSession.applicationContext.getPackageManager().getPackageInfo(packageName, 0).applicationInfo.flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0)
						attackSurface += "debuggable = true\n";
					
					String shared = currentSession.applicationContext.getPackageManager().getPackageInfo(packageName, 0).sharedUserId;
					
					if (shared != null)
						attackSurface += "shared user-id = " + currentSession.applicationContext.getPackageManager().getPackageInfo(packageName, 0).applicationInfo.uid + " (" + shared + ")\n";
					        	
					currentSession.sendFullTransmission(attackSurface, "");
				
				}
				catch (Throwable t)
				{
					currentSession.sendFullTransmission("", t.getMessage());
				}
				
			}
		}));
		
		
		//packages.path(package) - return path of apk and odex separated by \n
		commandList.add(new CommandWrapper("packages", "path", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Assign filter and permissions if they came in the arguments
				String packageName = Common.getParamString(argsArray, "packageName");
							
				//Get all packages from packagemanager
				PackageManager pm = currentSession.applicationContext.getPackageManager();
				List <PackageInfo> packages = pm.getInstalledPackages(PackageManager.GET_PERMISSIONS|PackageManager.GET_CONFIGURATIONS|PackageManager.GET_GIDS);
				
				String packagePath = "";
				
				//Iterate through packages
				for (PackageInfo package_:packages)
				{
					ApplicationInfo app = package_.applicationInfo; 
					
					//Check for package name
					if (app.packageName.equals(packageName))
					{
						packagePath = app.publicSourceDir;
						break;
					}
				}
				
				//Check if an odex file exists for the package
				if (new File(packagePath.replace(".apk", ".odex")).exists())
					packagePath += "\n" + packagePath.replace(".apk", ".odex");
				
				//Send to client
				currentSession.sendFullTransmission(packagePath, "");
			
			}
		}));
		
		
		
		
		/*************************************************************************************/
		/** Command section - SHELL
		/*************************************************************************************/
		
		//shell.execute(args) - perform shell command and give result
		commandList.add(new CommandWrapper("shell", "executeSingleCommand", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Get all the parameters
				String args = Common.getParamString(argsArray, "args");
				
				String returnValue = "";
				
				//Execute a Linux command and get result
				try
				{

					//Default working directory
					File workDir = new File("/");
					String [] env = null;
					
					//Executes the process using sh -c command (so that piping features etc. are present)
			        Process proc = Runtime.getRuntime().exec(new String[] {"sh", "-c", args}, env, workDir);
			        
			        //Wait for process to finish
			        try
			        {
			        	proc.waitFor();
			        }
			        catch (InterruptedException e) {}
			        
			        //Read output and error streams
			        BufferedReader reader = new BufferedReader(new InputStreamReader (proc.getInputStream()));
			        BufferedReader errorreader = new BufferedReader(new InputStreamReader (proc.getErrorStream()));

			        String line;
			        
			        //Display output and error streams
			        while ((line = errorreader.readLine()) != null)
			        	returnValue += line + "\n";
			        
			        while ((line = reader.readLine()) != null)
			        	returnValue += line + "\n";
			        
				}
				catch (Exception e)
				{
					currentSession.sendFullTransmission(e.getMessage(), "");
				}		
				
				currentSession.sendFullTransmission(returnValue.trim(), "");
				
				return ;
				
			}
		}));
		
		//shell.newMercuryShell() - make a new Shell
		commandList.add(new CommandWrapper("shell", "newMercuryShell", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				Common.mercuryShell = new Shell();
				currentSession.sendFullTransmission("", "");
				
			}
		}));
		
		//shell.executeMercuryShell() - execute a command on Mercury Shell
		commandList.add(new CommandWrapper("shell", "executeMercuryShell", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				//Get all the parameters
				String args = Common.getParamString(argsArray, "args");
				
				if (Common.mercuryShell.write(args))
					currentSession.sendFullTransmission("", "");
				else
					currentSession.sendFullTransmission("", "error");
				
			}
		}));
		
		//shell.readMercuryShell() - read from the Mercury Shell
		commandList.add(new CommandWrapper("shell", "readMercuryShell", new Executor()
		{
			
			@Override
			public void execute(List<ArgumentWrapper> argsArray, Session currentSession)
			{
				// TODO Auto-generated method stub
				
				currentSession.sendFullTransmission(Common.mercuryShell.read(), "");
				
			}
		}));
		
		
		
		

		
		
		
		
		
	}
	
}
