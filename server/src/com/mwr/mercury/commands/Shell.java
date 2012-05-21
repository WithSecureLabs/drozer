package com.mwr.mercury.commands;

import com.mwr.mercury.ArgumentWrapper;
import com.mwr.mercury.Common;
import com.mwr.mercury.Session;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.List;

public class Shell
{
	public static void executeSingleCommand(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		// Get all the parameters
		String args = Common.getParamString(argsArray, "args");

		String returnValue = "";

		// Execute a Linux command and get result
		try
		{

			// Default working directory
			File workDir = new File("/");
			String[] env = null;

			// Executes the process using sh -c command (so that piping features
			// etc. are present)
			Process proc = Runtime.getRuntime().exec(new String[]
			{ "sh", "-c", args }, env, workDir);

			// Wait for process to finish
			try
			{
				proc.waitFor();
			}
			catch (InterruptedException e)
			{
			}

			// Read output and error streams
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					proc.getInputStream()));
			BufferedReader errorreader = new BufferedReader(
					new InputStreamReader(proc.getErrorStream()));

			String line;

			// Display output and error streams
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

		return;
	}

	public static void newMercuryShell(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		Common.mercuryShell = new com.mwr.mercury.Shell();
		currentSession.sendFullTransmission("", "");
	}

	public static void executeMercuryShell(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		//Get all the parameters
		String args = Common.getParamString(argsArray, "args");
		
		if (Common.mercuryShell.write(args))
			currentSession.sendFullTransmission("", "");
		else
			currentSession.sendFullTransmission("", "error");
	}

	public static void readMercuryShell(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		currentSession.sendFullTransmission(Common.mercuryShell.read(), "");
	}
}
