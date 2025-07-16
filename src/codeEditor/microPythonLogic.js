import { useState, useEffect, useRef } from "react";

export const useMicroPython = () => {
  const [output, setOutput] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const micropythonRef = useRef(null);
  const outputBuffer = useRef([]);

  const initMicroPython = async () => {
    setIsLoading(true);
    setOutput("");
    try {
      const script = document.createElement("script");
      script.src = "/micropython.mjs";
      script.type = "module";
      script.async = true;

      script.onload = async () => {
        try {
          if (!window.loadMicroPython) {
            throw new Error(
              "loadMicroPython global not found. Available globals: " +
                Object.keys(window)
                  .filter((key) => key.toLowerCase().includes("python"))
                  .join(", ")
            );
          }

          const wasmResponse = await fetch("/micropython.wasm");
          if (!wasmResponse.ok) {
            throw new Error(
              `Failed to fetch micropython.wasm: ${wasmResponse.statusText}`
            );
          }
          const wasmBinary = await wasmResponse.arrayBuffer();

          const micropython = await window.loadMicroPython({
            wasmBinary,
            stdout: (text) => {
              outputBuffer.current.push(text);
              setOutput(outputBuffer.current.join(""));
            },
          });

          const possibleExecMethods = [
            "runPython",
            "exec",
            "eval",
            "runCode",
            "run_script",
            "execute",
          ];
          const execMethod = possibleExecMethods.find(
            (method) => typeof micropython[method] === "function"
          );
          if (!execMethod) {
            throw new Error(
              "No execution method found. Available methods: " +
                Object.getOwnPropertyNames(Object.getPrototypeOf(micropython))
                  .concat(Object.keys(micropython))
                  .join(", ")
            );
          }

          micropythonRef.current = {
            runCode: async (code) => {
              try {
                outputBuffer.current = [];
                await micropython[execMethod](code);
                return outputBuffer.current.join("");
              } catch (error) {
                throw new Error(`Execution failed: ${error.message}`);
              }
            },
            FS: micropython.FS,
          };

          // Create directory structure
          try {
            micropythonRef.current.FS.mkdir("/lib");
            micropythonRef.current.FS.mkdir("/lib/output_modules");
            micropythonRef.current.FS.mkdir("/lib/process_modules");
            micropythonRef.current.FS.mkdir("/lib/input_modules");
            micropythonRef.current.FS.mkdir("/lib/data_modules");
          } catch (e) {
            console.warn("Failed to create directories:", e);
          }

          // Preload modules
          const modules = [
            "electrical.py",
            "hello.py",
            "machine.py",
            "output_modules/st7565_spi.py",
            "process_modules/text_buffer.py",
            "process_modules/text_buffer_uploader.py",
            "process_modules/menu_buffer.py",
            "process_modules/menu_buffer_uploader.py",
            "process_modules/form_buffer.py",
            "process_modules/form_buffer_uploader.py",
            "process_modules/typer.py",
            "process_modules/navbar.py",
            "input_modules/keypad.py",
            "data_modules/keypad_map.py",
            "data_modules/characters.py",
          ];
          for (const mod of modules) {
            try {
              const response = await fetch(`/lib/${mod}`);
              if (!response.ok) {
                throw new Error(
                  `Failed to fetch /lib/${mod}: ${response.statusText}`
                );
              }
              const moduleContent = await response.text();
              micropythonRef.current.FS.writeFile(`/lib/${mod}`, moduleContent);
              const writtenContent = micropythonRef.current.FS.readFile(
                `/lib/${mod}`,
                { encoding: "utf8" }
              );
            } catch (moduleError) {
              console.error(`Failed to preload ${mod}:`, moduleError);
              setOutput(
                (prev) =>
                  `${prev}\nError: Failed to load module ${mod} - ${moduleError.message}`
              );
            }
          }

          // Update sys.path
          try {
            await micropythonRef.current.runCode(`
              import sys
              sys.path.append('/lib')
              sys.path.append('/lib/machine')
              sys.path.append('/lib/output_modules')
              sys.path.append('/lib/process_modules')
              sys.path.append('/lib/input_modules')
              sys.path.append('/lib/data_modules')
              print("sys.path:", sys.path)
              import utime
              `);
          } catch (pathError) {
            console.error("Failed to update sys.path:", pathError);
            setOutput(
              (prev) =>
                `${prev}\nError: Failed to set sys.path - ${pathError.message}`
            );
          }

          try {
            await micropythonRef.current.runCode(
              'print("MicroPython test successful")'
            );
            setOutput("");
          } catch (testError) {
            console.warn("Test execution failed:", testError);
            setOutput(
              `MicroPython initialized\nTest failed: ${testError.message}`
            );
          }

          setIsLoading(false);
        } catch (error) {
          console.error("Initialization error:", error);
          setOutput(
            `Error: Failed to initialize MicroPython - ${error.message}`
          );
          setIsLoading(false);
        }
      };

      script.onerror = () => {
        console.error("Failed to load micropython.mjs");
        setOutput(
          "Error: Failed to load MicroPython module (check /micropython.mjs in public folder)"
        );
        setIsLoading(false);
      };

      document.head.appendChild(script);
    } catch (error) {
      console.error("Setup error:", error);
      setOutput(`Error: ${error.message}`);
      setIsLoading(false);
    }
  };

  const runCode = async (code) => {
    if (isLoading) {
      setOutput("Please wait, MicroPython is still loading...");
      return;
    }
    if (!micropythonRef.current) {
      setOutput("Error: MicroPython not initialized");
      return;
    }

    try {
      outputBuffer.current = [];
      await micropythonRef.current.runCode(code);
      setOutput(outputBuffer.current.join("") || "No output");
    } catch (error) {
      console.error("Execution error:", error);
      setOutput(`Error: ${error.message}`);
    }
  };

  useEffect(() => {
    initMicroPython();
    return () => {
      const scripts = document.head.querySelectorAll(
        'script[src="/micropython.mjs"]'
      );
      scripts.forEach((script) => script.remove());
    };
  }, []);

  return { output, isLoading, runCode };
};