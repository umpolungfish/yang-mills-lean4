# Yang–Mills ELF build and Vox audit

Built the full Yang–Mills import bundle with `/home/mrnob0dy666/imsgct/lean2elf.sh`, using the project Lean 4.28.0 Lake environment and local package cache.

- Bundle: `YangMillsELFBundle.lean`, importing the project modules and checking the seven principal declarations and their kernel axiom reports.
- Build: `16,125` Lake jobs completed successfully.
- ELF: `yang-mills-full.elf`, x86-64 PIE with debug information, 213 MB.
- Runtime: prints `Program compiled from YangMillsELFBundle`.
- ELF SHA-256: `ab0af35ecb6c3b75cf125091162fd2ce3dfdfe845b2ad670dd62ee5dc0565e1a`.

Vox audited the complete image:

- Code image: `151,608,850` bytes; entry point `0xc1abc0`.
- Lifted by descent: `178,350` functions and `36,863,127` instructions.
- Fallback sweep: `1,137,627` additional functions.
- Coverage: `151,608,850 / 151,608,850` bytes.
- Verdicts: `T 13,206`, `B 195,443`, `N 1,107,328`, `F 0`.

The raw Vox output is in `vox_audit_fresh.txt`. The executable is retained locally as `yang-mills-full.elf`.
