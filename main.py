from src.writer import MotivAI
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a cover letter for a specified company.")
    parser.add_argument("-n", "--company_name", type=str, required=True, help="The name of the company to generate the cover letter for.")
    parser.add_argument("-l", "--language", type=str, required=False, default="fr" ,help="The language of the cover letter to generate.")
    parser.add_argument("-o", "--offer", type=str, required=False ,help="Path to the job offer to generate the cover letter for.")

    args = parser.parse_args()


    writer = MotivAI(language=args.language, offer_path=args.offer)
    writer.generate_cover_letter(args.company_name)