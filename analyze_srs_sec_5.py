#!/usr/bin/env python3
#-*- utf-8 -*-

import sys
import re

def print_srs_csv(srs_list):
    for s in srs_list:
        print('"%s","%s","%s","%s","%s","%s","%s","%s","%s"' %
              (s.item,
               s.abst.replace('"', '""'),
               s.srs_type.replace('"', '""'),
               s.srs_desc.replace('"', '""'),
               s.srs_rational.replace('"', '""'),
               s.srs_usecase.replace('"', '""'),
               s.srs_dependence.replace('"', '""'),
               s.srs_supmat.replace('"', '""'),
               s.srs_reference.replace('"', '""')) )

class Srs:
    def __init__(self):
        self.item = ''
        self.abst = ''
        self.srs_type = ''
        self.srs_desc = ''
        self.srs_rational = ''
        self.srs_usecase = ''
        self.srs_dependence = ''
        self.srs_supmat = ''
        self.srs_reference = ''

    def add_srs_type(self, buf):
        if self.srs_type:
            self.srs_type += ' ' + buf
        else:
            self.srs_type = buf

    def add_srs_desc(self, buf):
        if not self.srs_desc:
            self.srs_desc += ' ' + buf
        else:
            self.srs_desc = buf

    def add_srs_rational(self, buf):
        if self.srs_rational:
            self.srs_rational += ' ' + buf
        else:
            self.srs_rational = buf

    def add_srs_usecase(self, buf):
        if self.srs_usecase:
            self.srs_usecase = buf
        else:
            self.srs_usecase += ' ' + buf

    def add_srs_dependence(self, buf):
        if self.srs_dependence:
            self.srs_dependence += ' ' + buf
        else:
            self.srs_dependence = buf

    def add_srs_supmat(self, buf):
        if self.srs_supmat:
            self.srs_supmat += ' ' + buf
        else:
            self.srs_supmat = buf

class ParseSrs:
    STATE_NONE       = 0
    STATE_HEADER     = 1
    STATE_TYPE       = 2
    STATE_DESC       = 3
    STATE_RATIONAL   = 4
    STATE_USECASE    = 5
    STATE_DEPENDENCE = 6
    STATE_SUPMAT     = 7

    def __init__(self):
        self.state = self.STATE_NONE

    def parse_item(self, buf):
        item = re.sub(r'^.*\[S', '', buf)
        return re.sub(r'\].*$', '', item)

    def parse_abst(self, buf):
        return re.sub(r'^.*\[SRS_[a-zA-Z0-9]+_[0-9]+ *\] +', '', buf)
        
    def parse(self, buf):
        srs_list = []
        srs = None
        for line in buf:
            if not line:
                continue
            line = line.rstrip()
            if re.match(r'^[0-9.]+ *\[SRS_', line):
                if srs:
                    srs_list.append(srs)
                srs = Srs()
                srs.item = self.parse_item(line)
                srs.abst = self.parse_abst(line)
            elif re.match(r'^Type:.*$', line):
                self.state = self.STATE_TYPE
            elif re.match(r'^Description:.*$', line):
                self.state = self.STATE_DESC
            elif re.match(r'^Rationale:.*$', line):
                self.state = self.STATE_RATIONAL
            elif re.match(r'^Use Case:.*$', line):
                self.state = self.STATE_USECASE
            elif re.match(r'^Dependencies:.*$', line):
                self.state = self.STATE_DEPENDENCE
            elif re.match(r'^Supporting Material:.*$', line):
                self.state = self.STATE_SUPMAT
            elif re.match(r'^\. *\(.*\).*$', line):
                self.state = self.STATE_NONE
                line = re.sub(r'^.*\(', '', line)
                line = re.sub(r'\).*$', '', line)
                srs.srs_reference = line
                srs_list.append(srs)
                srs = None
            else:
                if self.state == self.STATE_TYPE:
                    srs.add_srs_type(line.strip())
                elif self.state == self.STATE_DESC:
                    srs.add_srs_desc(line)
                elif self.state == self.STATE_RATIONAL:
                    srs.add_srs_rational(line)
                elif self.state == self.STATE_USECASE:
                    srs.add_srs_usecase(line)
                elif self.state == self.STATE_DEPENDENCE:
                    srs.add_srs_dependence(line.replace('[','').replace(']',''))
                elif self.state == self.STATE_SUPMAT:
                    srs.add_srs_supmat(line)
        if srs:
            srs_list.append(srs)
        return srs_list

def line_modify(org_buf):
    buf = []
    pre_line = ''
    for line in org_buf:
        line = line.rstrip()
        if pre_line:
            if not line:
                buf.append(pre_line)
                pre_line = ''
            elif re.match(r'^\.', line):
                buf.append(pre_line)
                pre_line = line
            else:
                pre_line += ' ' + line
        else:
            if line:
                pre_line = line
            else:
                buf.append('')
    if pre_line:
        buf.append(pre_line)
    return buf

def pick_srs_sec_5(org_buf):
    num = 0
    # skip before section 5
    for line in org_buf:
        line = line.rstrip()
        if re.match(r'^5 Requirement Specification$', line):
            break
        num += 1
    start_num = num

    # skip to section 6
    for line in org_buf[num:]:
        line = line.rstrip()
        if re.match(r'^6 References*$', line):
            break
        num += 1
    return buf[start_num:num]

def print_usage():
    print('Usage: %s <srs_text>' % sys.argv[0])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        exit()

    with open(sys.argv[1]) as f:
        buf = f.readlines()
        buf = pick_srs_sec_5(buf)
        buf = line_modify(buf)
        p = ParseSrs()
        srs_list = p.parse(buf)
        print_srs_csv(srs_list)

# end of file

