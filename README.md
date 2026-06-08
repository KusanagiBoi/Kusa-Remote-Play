 # Kusa Remote Play


Kusa Remote Play is a bare-metal approach to remote gaming and application streaming, built natively for Linux. Traditional streaming clients often suffer from bloated network stacks, unpredictable latency spikes, and dependency conflicts across distributions. 


This project tackles those issues head-on by utilizing Secure Reliable Transport (SRT) alongside a custom GStreamer pipeline to ensure sub-second, glass-to-glass latency. Whether tunneling through a local area network or streaming across an encrypted tunnel, KRP delivers hardware-accelerated video decoding and highly responsive input redirection—capable of handling everything from standard gamepads to strict, frame-perfect arcade stick inputs.


Packaged as a fully self-contained Flatpak, it guarantees a consistent, pristine runtime environment on any machine, from a desktop PC to an ARM-based single-board computer.

---

### Architectural Choice: Why Containerize with Flatpak?


Developing a low-latency video streaming pipeline often leads straight into dependency hell. Managing conflicting GStreamer versions, missing SRT (Secure Reliable Transport) headers, and differing package managers across Linux distributions makes deployment highly unpredictable.


Kusa Remote Play bypasses these limitations by leveraging Flatpak as a strict dependency sandbox, rather than just a graphical app distribution method. The entire network transport layer (`libsrt`) and the necessary GStreamer plugins are compiled directly from source within the isolated container. 


This architectural approach guarantees:

* **Zero Host Pollution:** The host operating system remains untouched. No global installations of obscure network libraries are required.

* **Reproducible Runtime:** The networking and streaming execution environment is 100% identical regardless of the underlying host Linux distribution.

* **Cross-Architecture Parity:** Relying on the Freedesktop SDK ensures the application maintains perfect feature parity and stability across both `x86_64` desktop machines and `aarch64` embedded devices (e.g., Raspberry Pi).

---

## Installation & Usage

To install the application using the pre-compiled deployment package, follow these steps:

1. Go to the **Releases** section on GitHub and download the latest `Kusa-Remote-Play.zip`.
2. Extract the ZIP archive. It contains the installer script (`install.sh`) and the Flatpak bundles for both `x86_64` and `aarch64` architectures.
3. Open a terminal inside the extracted directory and execute the installation script:

\`\`\`bash
chmod +x install.sh
./install.sh
\`\`\`

*Note: The script automatically detects your hardware architecture via `uname -m`, checks for the Flatpak runtime presence, and provisions the correct bundle (`_x86_64` or `_aarch64`) locally.*

### Run

Once the installation script completes successfully, launch the application using:

\`\`\`bash
flatpak run ro.upt.KusaRemotePlay
\`\`\`

---

## Development & Building from Source

If you want to modify the source code or recompile the sandbox environment manually, use the following commands:

1. Compile the modules and application layer defined in the manifest:
\`\`\`bash
flatpak run org.flatpak.Builder --user --install --force-clean build-dir ro.upt.KusaRemotePlay.json
\`\`\`

2. Export the build directory and package it into a single-file bundle:
\`\`\`bash
flatpak build-export repo build-dir
flatpak build-bundle repo KusaRemotePlay_$(uname -m).flatpak ro.upt.KusaRemotePlay
\`\`\`

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
