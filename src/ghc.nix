let
   pkgs = import <nixpkgs> {};
 in
 { stdenv ? pkgs.stdenv,
   ghc    ? pkgs.ghc.ghc784,
   alex   ? pkgs.haskellPackages_ghc784_no_profiling.alex_3_1_3,
   happy  ? pkgs.haskellPackages_ghc784_no_profiling.happy }:

 stdenv.mkDerivation {
   name = "alex-happy";
   version = "0.1.0.0";
   src = ./.;
   buildInputs = [ ghc alex happy ];
}