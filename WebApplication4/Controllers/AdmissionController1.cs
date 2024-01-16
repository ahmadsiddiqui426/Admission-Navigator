using Microsoft.AspNetCore.Mvc;
using ConsoleApp1.Models;
using ConsoleApp1.Data;// Adjust namespace to your EF models
using System.Linq;
using System.Globalization;

public class AdmissionController : Controller
{
    private readonly UniContext _context; // Replace with your actual DbContext

    public AdmissionController(UniContext context)
    {
        _context = context;
    }

    public IActionResult FieldAdmissions(int id)
    {
        var currentDate = DateTime.Now.Date;

        // Define the date format
        var format = "dd-MM-yyyy";

        var admissions = _context.FieldAdmissions
            .Where(fa => fa.FieldId == id)
            .Join(_context.Admissions,
                  fa => fa.AdmissionId,
                  a => a.Id,
                  (fa, a) => a)
            .ToList(); // Fetch data into memory

        // Use DateTime.ParseExact with the specified format
        var openAdmissionsCount = admissions
            .Where(a => DateTime.ParseExact(a.Date, format, CultureInfo.InvariantCulture) >= currentDate)
            .Select(a => a.University)
            .Distinct()
            .Count();

        var fieldName = _context.Fields
                            .Where(f => f.FID == id)
                            .Select(f => f.Name)
                            .FirstOrDefault();

        ViewBag.OpenAdmissionsCount = openAdmissionsCount;
        ViewBag.FieldName = fieldName ?? "Unknown";
        // Filter the list for the view
        //admissions = admissions.Where(a => DateTime.ParseExact(a.Date, format, CultureInfo.InvariantCulture) >= currentDate).ToList();

        return View(admissions);
    }



}
