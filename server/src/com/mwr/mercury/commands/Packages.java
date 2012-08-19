// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.xmlpull.v1.XmlPullParser;

import android.content.pm.ActivityInfo;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.ProviderInfo;
import android.content.pm.ServiceInfo;
import android.content.res.AssetManager;
import android.content.res.XmlResourceParser;

import com.mwr.mercury.ArgumentWrapper;
import com.mwr.mercury.Common;
import com.mwr.mercury.Session;

public class Packages
{
	public static void info(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		currentSession.startTransmission();
		currentSession.startResponse();
		currentSession.startData();

		// Assign filter and permissions if they came in the arguments
		String filter = Common.getParamString(argsArray, "filter");
		String permissions = Common.getParamString(argsArray, "permissions");

		// Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext
				.getPackageManager();
		List<PackageInfo> packages = pm
				.getInstalledPackages(PackageManager.GET_PERMISSIONS
						| PackageManager.GET_CONFIGURATIONS
						| PackageManager.GET_GIDS
						| PackageManager.GET_SHARED_LIBRARY_FILES);

		// Iterate through packages
		for (PackageInfo currentPackage : packages)
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
			String[] libraries = app.sharedLibraryFiles;

			// Find all permissions that this app has requested
			String requestedPermissions = "";
			String[] requestedPermissionsArray = currentPackage.requestedPermissions;

			if (requestedPermissionsArray != null)
			{
				for (String permission : requestedPermissionsArray)
					requestedPermissions += permission + "; ";
			}

			String librariesString = "";
			if (libraries != null)
				for (int i = 0; i < libraries.length; i++)
					librariesString += libraries[i] + "; ";

			// Get the GIDs
			String gidString = "";
			if (gids != null)
				for (int z = 0; z < gids.length; z++)
					gidString += new Integer(gids[z]).toString() + "; ";

			boolean relevantFilter = filter != "";
			if (relevantFilter)
				relevantFilter = packageName.toUpperCase().contains(
						filter.toUpperCase())
						|| processName.toUpperCase().contains(
								filter.toUpperCase())
						|| dataDir.toUpperCase().contains(filter.toUpperCase())
						|| publicSourceDir.toUpperCase().contains(
								filter.toUpperCase())
						|| (uid.toString().equals(filter));

			boolean relevantPermissions = permissions != "";
			if (relevantPermissions)
				relevantPermissions = requestedPermissions.toUpperCase()
						.contains(permissions.toUpperCase());

			boolean bothFiltersPresent = false;
			if ((filter != "") && (permissions != ""))
				bothFiltersPresent = true;

			boolean bothFiltersRelevant = false;
			if (bothFiltersPresent && relevantFilter && relevantPermissions)
				bothFiltersRelevant = true;

			boolean noFilters = (filter.length() == 0)
					&& (permissions.length() == 0);

			// Apply filter
			if ((bothFiltersPresent && bothFiltersRelevant)
					|| (!bothFiltersPresent && (relevantFilter || relevantPermissions))
					|| (!bothFiltersPresent && noFilters))
			{
				currentSession
						.send("Package name: " + packageName + "\n", true);
				currentSession
						.send("Process name: " + processName + "\n", true);
				currentSession.send("Version: " + version + "\n", true);
				currentSession.send("Data directory: " + dataDir + "\n", true);
				currentSession
						.send("APK path: " + publicSourceDir + "\n", true);
				currentSession.send("UID: " + uid + "\n", true);
				currentSession.send("GID: " + gidString + "\n", true);

				if (librariesString.length() > 0)
					currentSession.send("Shared libraries: " + librariesString
							+ "\n", true);

				if (sharedUserId != null)
					currentSession.send("SharedUserId: " + sharedUserId + " ("
							+ uid + ")\n", true);

				currentSession.send("Permissions: " + requestedPermissions
						+ "\n\n", true);

			}
		}

		currentSession.endData();
		currentSession.noError();
		currentSession.endResponse();
		currentSession.endTransmission();
	}

	public static void sharedUid(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		currentSession.startTransmission();
		currentSession.startResponse();
		currentSession.startData();

		// Get all the parameters
		String filter = Common.getParamString(argsArray, "uid");

		// Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext
				.getPackageManager();
		List<PackageInfo> packages = pm
				.getInstalledPackages(PackageManager.GET_PERMISSIONS);

		List<Integer> uidList = new ArrayList<Integer>();

		// Get all UIDs
		for (PackageInfo package_ : packages)
		{
			ApplicationInfo app = package_.applicationInfo;

			if (!uidList.contains(app.uid))
				uidList.add(app.uid);
		}

		// Iterate through packages
		for (Integer uid : uidList)
		{
			String[] packageNames = pm.getPackagesForUid(uid);
			String accumulatedPermissions = "";

			if ((filter.length() > 0 && filter.equals(uid.toString()))
					|| filter.length() == 0)
			{
				currentSession.send(
						"UID: " + uid + " (" + pm.getNameForUid(uid) + ")\n",
						true);

				if (packages != null)
				{
					for (int s = 0; s < packageNames.length; s++)
					{
						// Get package permissions and add to list of
						// accumulated
						PackageInfo pack = null;

						try
						{
							pack = currentSession.applicationContext
									.getPackageManager().getPackageInfo(
											packageNames[s],
											PackageManager.GET_PERMISSIONS);
						}
						catch (Exception e)
						{
						}

						String[] requestedPermissionsArray = pack.requestedPermissions;

						if (requestedPermissionsArray != null)
						{
							for (String permission : requestedPermissionsArray)
								if (!accumulatedPermissions
										.contains(permission))
									accumulatedPermissions += permission + "; ";
						}

						currentSession.send("Package name: " + packageNames[s]
								+ "\n", true);
					}

				}

				// Send accumulated permissions
				currentSession.send("Accumulated permissions: "
						+ accumulatedPermissions + "\n", true);

				currentSession.send("\n", true);
			}
		}

		currentSession.endData();
		currentSession.noError();
		currentSession.endResponse();
		currentSession.endTransmission();
	}

	public static void attackSurface(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		// Get all the parameters
		String packageName = Common.getParamString(argsArray, "packageName");

		try
		{

			// Check number of exported activities
			int numActivities = 0;

			ActivityInfo[] activities = currentSession.applicationContext
					.getPackageManager().getPackageInfo(packageName,
							PackageManager.GET_ACTIVITIES).activities;
			if (activities != null)
				for (int i = 0; i < activities.length; i++)
					if (activities[i].exported)
						numActivities++;

			// Check number of exported receivers
			int numReceivers = 0;
			ActivityInfo[] receivers = currentSession.applicationContext
					.getPackageManager().getPackageInfo(packageName,
							PackageManager.GET_RECEIVERS).receivers;
			if (receivers != null)
				for (int i = 0; i < receivers.length; i++)
					if (receivers[i].exported)
						numReceivers++;

			// Check number of exported providers
			int numProviders = 0;
			ProviderInfo[] providers = currentSession.applicationContext
					.getPackageManager().getPackageInfo(packageName,
							PackageManager.GET_PROVIDERS).providers;
			if (providers != null)
				for (int i = 0; i < providers.length; i++)
					if (providers[i].exported)
						numProviders++;

			// Check number of exported services
			int numServices = 0;
			ServiceInfo[] services = currentSession.applicationContext
					.getPackageManager().getPackageInfo(packageName,
							PackageManager.GET_SERVICES).services;
			if (services != null)
				for (int i = 0; i < services.length; i++)
					if (services[i].exported)
						numServices++;

			String attackSurface = "";
			attackSurface += numActivities + " activities exported\n";
			attackSurface += numReceivers + " broadcast receivers exported\n";
			attackSurface += numProviders + " content providers exported\n";
			attackSurface += numServices + " services exported\n\n";

			if ((currentSession.applicationContext.getPackageManager()
					.getPackageInfo(packageName, 0).applicationInfo.flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0)
				attackSurface += "debuggable = true\n";

			String shared = currentSession.applicationContext
					.getPackageManager().getPackageInfo(packageName, 0).sharedUserId;

			if (shared != null)
				attackSurface += "shared user-id = "
						+ currentSession.applicationContext.getPackageManager()
								.getPackageInfo(packageName, 0).applicationInfo.uid
						+ " (" + shared + ")\n";

			currentSession.sendFullTransmission(attackSurface, "");

		}
		catch (Throwable t)
		{
			currentSession.sendFullTransmission("", t.getMessage());
		}
	}

	public static void path(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		// Assign filter and permissions if they came in the arguments
		String packageName = Common.getParamString(argsArray, "packageName");

		// Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext
				.getPackageManager();
		List<PackageInfo> packages = pm
				.getInstalledPackages(PackageManager.GET_PERMISSIONS
						| PackageManager.GET_CONFIGURATIONS
						| PackageManager.GET_GIDS);

		String packagePath = "";

		// Iterate through packages
		for (PackageInfo package_ : packages)
		{
			ApplicationInfo app = package_.applicationInfo;

			// Check for package name
			if (app.packageName.equals(packageName))
			{
				packagePath = app.publicSourceDir;
				break;
			}
		}

		// Check if an odex file exists for the package
		if (new File(packagePath.replace(".apk", ".odex")).exists())
			packagePath += "\n" + packagePath.replace(".apk", ".odex");

		// Send to client
		currentSession.sendFullTransmission(packagePath, "");
	}
	
	
	//Return the manifest of the package in XML text
	public static void manifest(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		// Get all the parameters
		String packageName = Common.getParamString(argsArray, "packageName");

		try
		{

			//Open the AndroidManifest.xml of given package
			AssetManager am = currentSession.applicationContext.createPackageContext(packageName, 0).getAssets();
	        XmlResourceParser xml = am.openXmlResourceParser("AndroidManifest.xml");

	        StringBuilder output = new StringBuilder();
	        
	        //XML parsing
	        while (xml.next() != XmlPullParser.END_DOCUMENT) {
	        	switch (xml.getEventType()) {
	        		case XmlPullParser.START_TAG:
	        			output.append("<");
	        			output.append(xml.getName());
	        			for (int i = 0; i < xml.getAttributeCount(); i++) {
	        				output.append(" ");
	        				output.append(xml.getAttributeName(i));
	        				output.append("=\"");
	        				output.append(xml.getAttributeValue(i));
	        				output.append("\"");
	        			}
	        			output.append(">\n");
	        			break;
	        		case XmlPullParser.END_TAG:
	        			output.append("</");
	        			output.append(xml.getName());
	        			output.append(">\n");
	        			break;
	        		case XmlPullParser.TEXT:
	        			output.append(xml.getText());
	        			output.append("\n");
	        			break;
	        		default:
	        			break;
	        	}
	        }

			currentSession.sendFullTransmission(output.toString(), "");

		}
		catch (Throwable t)
		{
			currentSession.sendFullTransmission("", t.getMessage());
		}
	}


}
