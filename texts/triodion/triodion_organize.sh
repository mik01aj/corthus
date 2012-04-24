#!/bin/bash

#mv -iv Triod_02-Przedpocie_A.pl.txt 01_Nedelja_o_mytare_i_farisee.pl.txt
#mv -iv Triod_02-Przedpocie_B.pl.txt 02_Nedelja_o_bludnom_syne.pl.txt
#mv -iv Triod_02-Przedpocie_C.pl.txt 03_Subbota_mjasopustnaja.pl.txt
#mv -iv Triod_02-Przedpocie_D.pl.txt 04_Nedelja_mjasopustnaja.pl.txt
#mv -iv Triod_02-Przedpocie_E.pl.txt 05_Syrnaja_sedmica_s_ponedelnika_po_pjatok.pl.txt
#mv -iv Triod_02-Przedpocie_F.pl.txt 06_Subbota_syropustnaja.pl.txt
#mv -iv Triod_02-Przedpocie_G.pl.txt 07_Nedelja_syropustnaja.pl.txt
#mv -iv Triod_03-Tydzień_I_A.pl.txt 08_Ponedelnik_pervoj_sedmicy.pl.txt
#mv -iv Triod_03-Tydzień_I_B.pl.txt 09_Vtornik_pervoj_sedmicy.pl.txt
#mv -iv Triod_03-Tydzień_I_C.pl.txt 10_Sreda_pervoj_sedmicy.pl.txt
#mv -iv Triod_03-Tydzień_I_D.pl.txt 11_Chetverg_pervoj_sedmicy.pl.txt
#mv -iv Triod_03-Tydzień_I_E.pl.txt 12_Pjatok_pervoj_sedmicy.pl.txt
#mv -iv Triod_03-Tydzień_I_F.pl.txt 13_Subbota_pervoj_sedmicy.pl.txt
#mv -iv Triod_03-Tydzień_I_G.pl.txt 14_Nedelja_Torzhestva_Pravoslavija.pl.txt
#mv -iv Triod_04-Tydzień_II_A.pl.txt 15_Vtoraja_sedmica_s_ponedelnika_po_pjatok.pl.txt
#mv -iv Triod_04-Tydzień_II_B.pl.txt 16_Subbota_vtoroj_sedmicy.pl.txt
#mv -iv Triod_04-Tydzień_II_C.pl.txt 17_Nedelja_vtoroj_sedmicy,_Grigorija_Palamy.pl.txt
#mv -iv Triod_05-Tydzień_III_A.pl.txt 18_Tretja_sedmica_s_ponedelnika_po_pjatok.pl.txt
#mv -iv Triod_05-Tydzień_III_B.pl.txt 19_Subbota_tretej_sedmicy.pl.txt
#mv -iv Triod_05-Tydzień_III_C.pl.txt 20_Nedelja_Krestopoklonnaja.pl.txt
#mv -iv Triod_06-Tydzień_IV_A.pl.txt 21_Chetvertaja_sedmica_s_ponedelnika_po_pjatok.pl.txt
#mv -iv Triod_06-Tydzień_IV_B.pl.txt 22_Subbota_chetvertoj_sedmicy.pl.txt
#mv -iv Triod_06-Tydzień_IV_C.pl.txt 23_Nedelja_chetvertoj_sedmicy,_Ioanna_Lestvichnika.pl.txt
#mv -iv Triod_07-Tydzień_V_A.pl.txt 24_A_Pjataja_sedmica_s_ponedelnika_po_pjatok.pl.txt
#mv -iv Triod_07-Tydzień_V_B.pl.txt 24_B_Mariino_stojanie_s_prilozheniem_sluzhby_sredy_s_alfavitnymi_stihirami.pl.txt
#mv -iv Triod_07-Tydzień_V_C.pl.txt 24_C_Pjataja_sedmica_s_ponedelnika_po_pjatok.pl.txt
#mv -iv Triod_07-Tydzień_V_D.pl.txt 26_Subbota_Akafista.pl.txt
#mv -iv Triod_07-Tydzień_V_E.pl.txt 27_Nedelja_pjatoj_sedmicy,_Marii_Egipetskoj.pl.txt
#mv -iv Triod_08-Tydzien_VI_A.pl.txt 28_Sedmica_vaij_s_ponedelnika_po_pjatok.pl.txt
#mv -iv Triod_08-Tydzien_VI_B.pl.txt 29_Lazareva_Subbota.pl.txt
#mv -iv Triod_08-Tydzien_VI_C.pl.txt 30_Nedelja_vaij_Verbnoe_Voskresene.pl.txt
#mv -iv Triod_09-Tydzien_Meki_A.pl.txt 31_Velikij_Ponedelnik.pl.txt
#mv -iv Triod_09-Tydzien_Meki_B.pl.txt 32_Velikij_Vtornik.pl.txt
#mv -iv Triod_09-Tydzien_Meki_C.pl.txt 33_Velikaja_Sreda.pl.txt
#mv -iv Triod_09-Tydzien_Meki_D.pl.txt 34_Velikij_Chetverg.pl.txt
#mv -iv Triod_10-Wielki_Piatek.pl.txt 35_Velikij_Pjatok.pl.txt
#mv -iv Triod_11-Wielka_Sobota.pl.txt 36_Velikaja_Subbota.pl.txt


# DANGEROUS!
# This will empty e.g. 01_Nedelja_o_mytare_i_farisee.el.txt
# if PubPharSun.el.txt wouldn't exist!

#cat PubPharSun.el.txt > 01_Nedelja_o_mytare_i_farisee.el.txt
#cat ProdigalSun.el.txt > 02_Nedelja_o_bludnom_syne.el.txt
#cat t17.el.txt > 03_Subbota_mjasopustnaja.el.txt
#cat LastJudgeSun.el.txt > 04_Nedelja_mjasopustnaja.el.txt
#cat t{22,23,24,25,26}.el.txt > 05_Syrnaja_sedmica_s_ponedelnika_po_pjatok.el.txt
#cat t27.el.txt > 06_Subbota_syropustnaja.el.txt
#cat CheeseSun.el.txt > 07_Nedelja_syropustnaja.el.txt
#cat t32.el.txt > 08_Ponedelnik_pervoj_sedmicy.el.txt
#cat t33.el.txt > 09_Vtornik_pervoj_sedmicy.el.txt
#cat t34.el.txt > 10_Sreda_pervoj_sedmicy.el.txt
#cat t35.el.txt > 11_Chetverg_pervoj_sedmicy.el.txt
#cat t36.el.txt > 12_Pjatok_pervoj_sedmicy.el.txt
#cat t37.el.txt > 13_Subbota_pervoj_sedmicy.el.txt
#cat orthodoxy.el.txt > 14_Nedelja_Torzhestva_Pravoslavija.el.txt
#cat t{42,43,44,45,46}.el.txt > 15_Vtoraja_sedmica_s_ponedelnika_po_pjatok.el.txt
#cat t47.el.txt > 16_Subbota_vtoroj_sedmicy.el.txt
#cat 2Palamas.el.txt > 17_Nedelja_vtoroj_sedmicy,_Grigorija_Palamy.el.txt
#cat t{52,53,54,55,56}.el.txt > 18_Tretja_sedmica_s_ponedelnika_po_pjatok.el.txt
#cat t57.el.txt > 19_Subbota_tretej_sedmicy.el.txt
#cat cross.el.txt > 20_Nedelja_Krestopoklonnaja.el.txt
#cat t{62,63,64,65,66}.el.txt > 21_Chetvertaja_sedmica_s_ponedelnika_po_pjatok.el.txt
#cat t67.el.txt > 22_Subbota_chetvertoj_sedmicy.el.txt
#cat 4Climakos.el.txt > 23_Nedelja_chetvertoj_sedmicy,_Ioanna_Lestvichnika.el.txt
#cat t{72,73}.el.txt > 24_A_Pjataja_sedmica_s_ponedelnika_po_pjatok_A.el.txt
#cat t74.el.txt > 24_B_Mariino_stojanie_s_prilozheniem_sluzhby_sredy_s_alfavitnymi_stihirami.el.txt
#cat t{75,76}.el.txt > 24_C_Pjataja_sedmica_s_ponedelnika_po_pjatok_C.el.txt
#cat t77.el.txt > 26_Subbota_Akafista.el.txt
#cat Egypt.el.txt > 27_Nedelja_pjatoj_sedmicy,_Marii_Egipetskoj.el.txt
#cat t{82,83,84,85,86}.el.txt > 28_Sedmica_vaij_s_ponedelnika_po_pjatok.el.txt
#cat t87.el.txt > 29_Lazareva_Subbota.el.txt
#cat Palms.el.txt > 30_Nedelja_vaij_Verbnoe_Voskresene.el.txt
#cat t92.el.txt > 31_Velikij_Ponedelnik.el.txt
#cat t93.el.txt > 32_Velikij_Vtornik.el.txt
#cat t94.el.txt > 33_Velikaja_Sreda.el.txt
#cat t95.el.txt > 34_Velikij_Chetverg.el.txt
#cat t96.el.txt > 35_Velikij_Pjatok.el.txt
#cat t97.el.txt > 36_Velikaja_Subbota.el.txt
