from vlsirtools.spice.ngspice import NGSpiceSim

class WebAssembly_NGspice(NGSpiceSim):
    """
    State and execution logic for a web assembly NGSpice-call to `vsp.Sim`.
    """
    @staticmethod
    def available() -> bool:
        """Boolean indication of whether the current running environment includes the simulator executable."""
        try:
            Module.run("-v")
            # subprocess.run(
            #     f"{NGSPICE_EXECUTABLE} -v",
            #     shell=True,
            #     check=True,
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE,
            #     timeout=10,
            # )
        except Exception:
            # Indicate "not available" for any Exception. Usually this will be a `subprocess.CalledProcessError`.
            return False
        return True  # Otherwise, installation looks good.
    def run(self) -> SimResult:
        """Run the specified `SimInput` in directory `self.rundir`, returning its results."""

        # Write the netlist
        self.write_netlist()

        self.run_sim_process()

        # Handle stdout and stderr as needed
        # Parse up the results
        return self.parse_results()

    def write_netlist(self) -> None:
        """# Write our netlist to file"""

        netlist_file = self.open("netlist.sp", "w")
        netlister = NgspiceNetlister(dest=netlist_file)
        netlister.write_sim_input(self.inp)
        netlist_file.flush()
        netlist_file.close()

    def parse_results(self) -> SimResult:
        """# Parse output data"""

        data = parse_nutbin(self.open("netlist.raw", "rb"))
        an_type_dispatch = dict(
            ac=self.parse_ac,
            dc=self.parse_dc,
            op=self.parse_op,
            tran=self.parse_tran,
            noise=self.parse_noise,
        )
        an_name_dispatch = dict(
            op="Plotname: Operating Point\n",
            dc="Plotname: DC Analysis\n",
            ac="Plotname: AC Analysis\n",
            tran="Plotname: Transient Analysis\n",
            noise="FIXME! do we still want this setup?",
        )
        results = []
        for an in self.inp.an:
            an_type = an.WhichOneof("an")
            inner = getattr(an, an_type)

            if an_type == "noise":
                # FIXME: I read somewhere that "Special cases aren't special enough to break the rules."
                results.append(self.parse_noise(inner, data))
                continue

            if an_type not in an_type_dispatch:
                msg = f"Invalid or Unsupported analysis {an} with type {an_type}"
                raise RuntimeError(msg)
            func = an_type_dispatch[an_type]
            analysis_name = an_name_dispatch[an_type]
            if analysis_name not in data:
                msg = f"Cannot read results for analysis {an}"
                raise RuntimeError(msg)
            inner_data = data[analysis_name]
            an_results = func(inner, inner_data)
            results.append(an_results)

        return SimResult(an=results)

    def parse_ac(self, an: vsp.AcInput, nutbin: "NutBinAnalysis") -> AcResult:
        # FIXME: the `mt0` and friends file names collide with tran, if they are used in the same Sim!
        measurements = self.get_measurements("*.mt*")

        # Pop the frequence vector out of the data
        freq = nutbin.data.pop("frequency")

        # Nutbin format stores the frequency vector as complex numbers, along with all the complex-valued signal data.
        # NOTE: once upon a time, we checked that the imaginary part of all frequencies was zero.
        # And that used to work! Now it doesn't; ngspice just seemingly leaves it uninitialized, or set to some random value.
        # See https://github.com/Vlsir/Vlsir/issues/66
        # Now, just grab the real part.
        freq = freq.real

        return AcResult(
            analysis_name=an.analysis_name,
            freq=freq,
            data=nutbin.data,
            measurements=measurements,
        )

    def parse_dc(self, an: vsp.DcInput, nutbin: "NutBinAnalysis") -> DcResult:
        measurements = self.get_measurements("*.ms*")
        return DcResult(
            analysis_name=an.analysis_name,
            indep_name=an.indep_name,
            data=nutbin.data,
            measurements=measurements,
        )

    def parse_op(self, an: vsp.OpInput, nutbin: "NutBinAnalysis") -> OpResult:
        return OpResult(
            analysis_name=an.analysis_name,
            data={k: v[0] for k, v in nutbin.data.items()},
        )

    def parse_tran(self, an: vsp.TranInput, nutbin: "NutBinAnalysis") -> TranResult:
        """Extract the results for Analysis `an` from `data`."""
        measurements = self.get_measurements("*.mt*")
        return TranResult(
            analysis_name=an.analysis_name, data=nutbin.data, measurements=measurements
        )

    def parse_noise(
        self, an: vsp.NoiseInput, nutbin: Mapping[str, "NutBinAnalysis"]
    ) -> NoiseResult:
        # Noise results come in two "analyses": the frequency-sweep data, and the integrated noise.
        # Collate them into a `NoiseResult`
        # FIXME: add measurements (if there are such things?)
        noise_sweep_data = nutbin.get("Plotname: Noise Spectral Density Curves\n", None)
        if noise_sweep_data is None:
            raise RuntimeError
        integrated_noise = nutbin.get("Plotname: Integrated Noise\n", None)
        if integrated_noise is None:
            raise RuntimeError
        return NoiseResult(
            analysis_name=an.analysis_name,
            data=noise_sweep_data,
            integrated_noise=integrated_noise,
            measurements={},
        )

    def get_measurements(self, filepat: str) -> Dict[str, float]:
        """Get the measurements at files matching (glob) `filepat`.
        Returns only a single files-worth of measurements, and issues a warning if more than one such file exists.
        Returns an empty dictionary if no matching files are found."""
        meas_files = list(self.glob(filepat))
        if not meas_files:
            return dict()
        if len(meas_files) > 1:
            msg = f"Unsupported: more than one measurement-file generated. Only the first will be read"
            warn(msg)
        return parse_mt0(self.open(meas_files[0], "r"))

    def run_sim_process(self) -> None:
        """Run a NGSpice sub-process, executing the simulation"""
        # Note the `nutbin` output format is dictated here
        cmd = shlex.split(f"{NGSPICE_EXECUTABLE} -b netlist.sp -r netlist.raw")
        return self.run_subprocess(cmd)

