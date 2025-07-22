"""
psych_support.py - Psychological support routines for AGI-EGGS

Provides trauma-informed, crisis psychology scripts for emotional stabilization
during disasters and high-stress scenarios. Includes breathing exercises,
decision paralysis override, moral injury processing, and positive reinforcement.

Usage:
    from modules.psych_support import CalmMode

    CalmMode.guide_breathing()
    CalmMode.override_decision_paralysis()
"""

class CalmMode:
    @staticmethod
    def guide_breathing():
        return (
            "Let's do a calming breathing exercise. Inhale slowly for 4 seconds, "
            "hold for 4 seconds, exhale for 6 seconds. Repeat 5 times."
        )

    @staticmethod
    def override_decision_paralysis():
        return (
            "If you're unsure what to do, break tasks into small steps. Choose one "
            "action you can do now, even if it's just checking your water supply or "
            "moving to a safer spot."
        )

    @staticmethod
    def positive_reinforcement():
        return (
            "You are capable. Every small action you take increases your safety. "
            "Keep going—you're doing well under pressure."
        )

    @staticmethod
    def process_moral_injury():
        return (
            "War and disaster force hard choices. If you feel guilt or distress, "
            "remember: survival choices are not moral failures. Focus on helping yourself and others."
        )
