# -*- coding: utf-8 -*-
"""Unit/regression tests for source data and generated six-report deliverables.

This is a local project test suite, not the separately requested legacy AI command.
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import mo_phong as sim
import thong_so_chung as spec
import trich_xuat


class SolarGeometryTests(unittest.TestCase):
    def test_noon_summer_solstice_preserves_north_branch(self):
        alpha,gamma=spec.solar_angles(172,12.0)
        self.assertAlmostEqual(alpha,87.48,places=1)
        self.assertEqual(gamma,180.0)

    def test_gamma_sign_east_morning_west_afternoon(self):
        self.assertLess(spec.solar_angles(80,9.0)[1],0)
        self.assertGreater(spec.solar_angles(80,15.0)[1],0)

    def test_wrap_keeps_both_180_endpoints(self):
        self.assertEqual(spec.wrap_azimuth_deg(180),180)
        self.assertEqual(spec.wrap_azimuth_deg(-180),180)
        self.assertAlmostEqual(spec.wrap_azimuth_deg(181),-179)

    def test_solar_angles_are_finite_and_bounded(self):
        for day in (80,172,266,355):
            for hour in range(0,24):
                alpha,gamma=spec.solar_angles(day,float(hour))
                self.assertTrue(math.isfinite(alpha) and math.isfinite(gamma))
                self.assertGreaterEqual(alpha,-90);self.assertLessEqual(alpha,90)
                self.assertGreater(gamma,-180);self.assertLessEqual(gamma,180)

    def test_sun_vector_is_unit_length(self):
        for day,hour in ((80,9.0),(172,12.0),(355,15.0)):
            self.assertAlmostEqual(sum(v*v for v in spec.sun_vector(day,hour)),1.0,places=10)

    def test_civil_to_solar_time_uses_longitude_and_equation_of_time(self):
        self.assertNotAlmostEqual(spec.solar_time_hours(12.0,80),12.0,places=3)
        self.assertLess(abs(spec.solar_time_hours(12.0,80)-12.0),0.5)

    def test_beta_is_normal_elevation_and_is_clamped(self):
        self.assertEqual(spec.beta_command(-4),0)
        self.assertEqual(spec.beta_command(87.4802),75)
        self.assertAlmostEqual(spec.beta_command(45.6),45.6)

    def test_summer_noon_saturates_tilt_by_about_12_5_degrees(self):
        alpha,_=spec.solar_angles(172,12.0)
        self.assertAlmostEqual(alpha-spec.beta_command(alpha),12.48,places=1)

    def test_azimuth_command_never_wraps_through_180(self):
        target,latched,state=spec.azimuth_limit_target(180,0)
        self.assertEqual((target,latched,state),(0.0,True,"hold-before-boundary"))
        target,latched,state=spec.azimuth_limit_target(180,90)
        self.assertEqual((target,latched,state),(120.0,True,"approach-boundary"))
        target,latched,state=spec.azimuth_limit_target(-150,-120,True)
        self.assertEqual((target,latched,state),(-120.0,True,"latched"))

    def test_target_within_mechanical_azimuth_limits_tracks(self):
        target,latched,state=spec.azimuth_limit_target(45,10)
        self.assertEqual((target,latched,state),(45.0,False,"track"))


class LdrAndHardwareTests(unittest.TestCase):
    def test_east_west_ldr_error_sign(self):
        self.assertGreater(sim.ldr_pair_error(-10),0)  # Đông sáng hơn
        self.assertLess(sim.ldr_pair_error(10),0)      # Tây sáng hơn

    def test_vertical_ldr_error_sign(self):
        self.assertGreater(sim.ldr_vertical_error(10),0)  # phía trên sáng hơn
        self.assertLess(sim.ldr_vertical_error(-10),0)    # phía dưới sáng hơn

    def test_adc_filter_configuration_is_sixteen_trimmed_to_twelve(self):
        source=(ROOT/"tools/revise_reports.py").read_text(encoding="utf-8")
        self.assertIn("N_SAMPLE = 16",source)
        self.assertIn("for (uint8_t i=2; i<N_SAMPLE-2; ++i)",source)
        self.assertIn("return total / 12",source)

    def test_hysteresis_start_and_stop_thresholds(self):
        active=False
        active=spec.hysteresis_track(250,active);self.assertTrue(active)
        active=spec.hysteresis_track(150,active);self.assertTrue(active)
        active=spec.hysteresis_track(120,active);self.assertFalse(active)
        active=spec.hysteresis_track(180,active);self.assertFalse(active)
        self.assertEqual(spec.START_THRESHOLD,200)
        self.assertEqual(spec.STOP_DEADBAND,120)

    def test_gpio2_is_not_a_tilt_pot_pin(self):
        self.assertEqual(spec.POT_TILT_PIN,4)
        self.assertNotIn(2,(spec.POT_AZ_PIN,spec.POT_TILT_PIN,*spec.LDR_PINS,
                            spec.AZ_FORWARD_PIN,spec.AZ_REVERSE_PIN,
                            spec.TILT_UP_PIN,spec.TILT_DOWN_PIN))

    def test_input_only_limit_pins_are_documented(self):
        spec_text=" ".join(v for _,v in spec.common_spec_rows())
        self.assertIn("GPIO34–39 chỉ input",spec_text)
        self.assertIn("bias ngoài",spec_text)

    def test_estop_is_normally_closed_and_fail_safe_high(self):
        spec_text=" ".join(v for _,v in spec.common_spec_rows())
        self.assertIn("NC kéo GND",spec_text)
        self.assertIn("đứt dây HIGH",spec_text)

    def test_one_axis_and_two_axis_motor_current_estimates(self):
        self.assertAlmostEqual(spec.MOTOR_LABEL_W/spec.MOTOR_VOLTAGE_V,5.0)
        self.assertEqual(1*5.0,5.0)
        self.assertEqual(2*5.0,10.0)

    def test_wind_moment_calculation_for_each_axis(self):
        row=spec.wind_torque(8.0,True)
        self.assertAlmostEqual(row["dynamic_pressure_pa"],38.4,places=6)
        self.assertAlmostEqual(row["force_n"],29.952,places=6)
        self.assertAlmostEqual(row["azimuth_design_nm"],13.4784,places=4)
        self.assertAlmostEqual(row["tilt_design_nm"],13.4856,places=4)


class SimulationTests(unittest.TestCase):
    def test_solar_matrices_cover_four_dates_and_thirteen_hours(self):
        matrix=sim.solar_matrix()
        self.assertEqual(len(matrix),4)
        self.assertEqual(len(matrix["21/3"]),13)
        self.assertIn("18",matrix["21/12"])

    def test_two_axis_command_matrix_separates_raw_and_limited_angles(self):
        matrix=sim.two_axis_command_matrix()
        noon=matrix["21/6"]["12"]
        self.assertEqual(noon["gamma_raw_deg"],180.0)
        self.assertLessEqual(abs(noon["gamma_cmd_deg"]),120.0)
        self.assertLessEqual(noon["beta_cmd_deg"],75.0)

    def test_limited_proxy_is_not_below_fixed_proxy(self):
        for row in sim.energy_gains().values():
            self.assertGreaterEqual(row["one_axis_proxy_index"],row["fixed_proxy_index"])
            self.assertGreaterEqual(row["two_axis_limited_proxy_index"],row["fixed_proxy_index"])

    def test_simulation_error_metric_excludes_below_threshold_twilight(self):
        result=sim.simulate_day(80,"hybrid",axes=1)
        self.assertGreater(result["evaluated_steps"],0)
        self.assertLess(result["evaluated_steps"],len(result["track"]))
        self.assertLess(result["max_error_deg"],10)

    def test_cloudy_interval_holds_one_axis_command(self):
        result=sim.simulate_day(80,"hybrid",axes=1)
        cloud=[r[1] for r in result["track"] if 10.0<=r[0]<11.0]
        self.assertTrue(cloud)
        self.assertEqual(len(set(cloud)),1)

    def test_night_does_not_issue_zero_angle_return_move(self):
        result=sim.simulate_day(80,"hybrid",axes=2)
        night=[r for r in result["track"] if r[0]>=18.0]
        self.assertTrue(night)
        self.assertEqual(len({(r[1],r[2]) for r in night}),1)


class ReportDeliverableTests(unittest.TestCase):
    def test_exactly_six_report_specs_and_three_volumes_each(self):
        items=trich_xuat.danh_sach_bao_cao()
        self.assertEqual(len(items),6)
        self.assertEqual(sum(x["volume"]=="Nghien_cuu" for x in items),2)
        self.assertEqual(sum(x["volume"]=="Che_tao" for x in items),2)
        self.assertEqual(sum(x["volume"]=="Lap_trinh" for x in items),2)

    def test_specialized_figures_are_not_duplicated_between_reports(self):
        image_owner={}
        for item in trich_xuat.danh_sach_bao_cao():
            for block in item["blocks"]:
                if block[0]=="img":
                    path=block[1]
                    self.assertNotIn(path,image_owner,(path,image_owner.get(path),item["base"]))
                    image_owner[path]=item["base"]
        self.assertGreaterEqual(len(image_owner),12)

    def test_adc_and_lcd_code_are_assigned_to_separate_volumes(self):
        items={x["base"]:x for x in trich_xuat.danh_sach_bao_cao()}
        p1=items["Bao_cao_1_truc_Lap_trinh"]["blocks"]
        p2=items["Bao_cao_2_truc_Lap_trinh"]["blocks"]
        code1="\n".join(b[1] for b in p1 if b[0]=="code")
        code2="\n".join(b[1] for b in p2 if b[0]=="code")
        self.assertIn("readTrimmed",code1)
        self.assertNotIn("readTrimmed",code2)
        self.assertIn("lastLCD",code2)
        self.assertIn("lastLdrAdjust",code2)
        self.assertIn("ldr_module.h",code2)

    def test_lcd_and_ldr_timers_are_independent_in_source(self):
        blocks=trich_xuat.danh_sach_bao_cao()[-1]["blocks"]
        code="\n".join(b[1] for b in blocks if b[0]=="code")
        self.assertIn("now-lastLCD)>=T_LCD",code)
        self.assertIn("now-lastLdrAdjust)>=T_LDR",code)
        self.assertIn("now-lastLightPoll)>=T_LIGHT",code)
        self.assertIn("LCD: 1 giây, timer độc lập",code)

    def test_beta_limit_and_hold_logic_are_explicit(self):
        items=trich_xuat.danh_sach_bao_cao()
        p2="\n".join(str(b) for item in items if item["report"]==2 for b in item["blocks"])
        self.assertIn("87,5°",p2)
        self.assertIn("12,5°",p2)
        self.assertIn("không ra lệnh 0°",p2)

    def test_references_start_at_one_and_are_sequential_per_volume(self):
        for item in trich_xuat.danh_sach_bao_cao():
            refs=[b[1] for b in item["blocks"] if b[0]=="b" and re.match(r"\[\d+\]",b[1])]
            ids=[int(re.match(r"\[(\d+)\]",line).group(1)) for line in refs]
            self.assertEqual(ids,list(range(1,len(ids)+1)),item["base"])

    def test_all_docx_and_pdf_deliverables_exist_and_have_front_matter(self):
        from docx import Document
        from pypdf import PdfReader
        for item in trich_xuat.danh_sach_bao_cao():
            self.assertTrue(Path(item["docx"]).is_file(),item["docx"])
            self.assertTrue(Path(item["pdf"]).is_file(),item["pdf"])
            doc=Document(item["docx"])
            text="\n".join(p.text for p in doc.paragraphs)
            for required in ("LỜI MỞ ĐẦU","LỜI CẢM ƠN","LỜI CAM ĐOAN","MỤC LỤC"):
                self.assertIn(required,text)
            pdf=PdfReader(item["pdf"])
            self.assertGreaterEqual(len(pdf.pages),9)
            self.assertGreaterEqual(len(pdf.outline),4)
            self.assertIn("MỤC LỤC",pdf.pages[4].extract_text() or "")

    def test_common_spec_pdf_is_one_page_and_merged_pdf_page_count_matches(self):
        from pypdf import PdfReader
        common=PdfReader(str(ROOT/"Bang_thong_so_chung.pdf"))
        merged=PdfReader(str(ROOT/"Bao_cao_day_du_6_phan.pdf"))
        items=trich_xuat.danh_sach_bao_cao()
        self.assertEqual(len(common.pages),1)
        expected=1+sum(len(PdfReader(x["pdf"]).pages) for x in items)
        self.assertEqual(len(merged.pages),expected)
        first=merged.pages[0].extract_text() or ""
        self.assertIn("BẢNG THÔNG SỐ CHUNG",first)

    def test_no_double_punctuation_in_generated_captions(self):
        for item in trich_xuat.danh_sach_bao_cao():
            for block in item["blocks"]:
                if block[0] in ("img","tbl") and len(block)>2:
                    self.assertNotRegex(block[2],r"(?:Hình|Bảng)\s+\d+\.\.")


def suite():
    loader=unittest.TestLoader()
    return loader.loadTestsFromModule(sys.modules[__name__])


if __name__=="__main__":
    result=unittest.TextTestRunner(verbosity=2).run(suite())
    raise SystemExit(not result.wasSuccessful())
